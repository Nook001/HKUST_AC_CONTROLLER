from PyQt6.QtCore import QObject, pyqtSignal
from config import Config

"""
User configurable application state.
Dynamic UI variables using PyQt6 signals/slots mechanism.
"""

class AppState(QObject):
    """Holds UI-bound state using PyQt6 signals.
    
    Signals are emitted when state changes, allowing UI components
    to react automatically without manual polling.
    
    Interval统一以 *分钟* 存储，需要秒的地方通过属性换算。
    """
    
    # 定义信号 - 当状态改变时自动发射
    ac_status_changed = pyqtSignal(object)  # bool or None
    is_running_changed = pyqtSignal(bool)
    next_check_time_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        # 内部状态变量
        self._ac_status = None
        self._token = ""
        self._interval_minutes = Config.INTERVAL_MIN
        self._next_check_time_str = "N/A"
        self._is_running = False

    # ==================== Properties (只读访问) ====================
    
    @property
    def ac_status_val(self) -> bool:
        """获取空调状态"""
        return self._ac_status

    @property
    def token(self) -> str:
        """获取原始 token（不含前缀）"""
        return self._token
    
    @token.setter
    def token(self, value: str):
        """设置 token"""
        self._token = value

    @property
    def token_val(self) -> str:
        """获取完整 token（含 Bearer 前缀）"""
        return Config.TOKEN_PREFIX + self._token

    @property
    def interval_minutes(self) -> int:
        """获取间隔分钟数"""
        return self._interval_minutes
    
    @interval_minutes.setter
    def interval_minutes(self, value: int):
        """设置间隔分钟数"""
        self._interval_minutes = value

    @property
    def interval_minutes_val(self) -> int:
        """获取间隔分钟数（别名，保持 API 兼容）"""
        return self._interval_minutes

    @property
    def interval_seconds_val(self) -> int:
        """获取间隔秒数"""
        return self._interval_minutes * 60

    @property
    def next_update_time_val(self) -> str:
        """获取下次检查时间字符串"""
        return self._next_check_time_str
    
    @property
    def is_running_val(self) -> bool:
        """获取运行状态"""
        return self._is_running

    # ==================== Public methods (状态修改) ====================
    
    def set_status(self, status: bool):
        """设置空调状态并发射信号"""
        if self._ac_status != status:
            self._ac_status = status
            self.ac_status_changed.emit(status)

    def set_next_update_time(self, time_str: str):
        """设置下次检查时间并发射信号"""
        if self._next_check_time_str != time_str:
            self._next_check_time_str = time_str
            self.next_check_time_changed.emit(time_str)

    def set_running(self, is_running: bool):
        """设置运行状态并发射信号"""
        if self._is_running != is_running:
            self._is_running = is_running
            self.is_running_changed.emit(is_running)