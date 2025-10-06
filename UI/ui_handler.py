import threading
import queue
from Controller.controller import ACController

def init_logic(window):
    """绑定逻辑函数为实例方法"""
    window.update_ui_on_state_change = lambda is_running: update_ui_on_state_change(window, is_running)
    window.update_status_display = lambda *args: update_status_display(window, *args)
    window.toggle_controller_loop = lambda: toggle_controller_loop(window)
    window.start_controller = lambda: start_controller(window)
    window.stop_controller = lambda: stop_controller(window)
    window.validate_interval = lambda: validate_interval(window)
    window.process_log_queue = lambda: process_log_queue(window)
    window.log_message = lambda message: log_message(window, message)

def finalize_logic(window):
    """在 UI 构建完成后绑定状态监听"""
    # 使用 PyQt6 信号槽机制替代 Tkinter 的 trace_add
    window.app_state.is_running_changed.connect(window.update_ui_on_state_change)
    window.app_state.ac_status_changed.connect(window.update_status_display)
    window.app_state.next_check_time_changed.connect(
        lambda time_str: window.next_check_label.setText(time_str)
    )

def update_ui_on_state_change(window, is_running: bool):
    """当运行状态改变时更新 UI"""
    # 更新按钮文字
    window.switch_button.setText("Stop" if is_running else "Start")
    
    # 启用/禁用输入框
    window.token_entry.setEnabled(not is_running)
    window.interval_entry.setEnabled(not is_running)
    
    # 如果停止，重置下次检查时间
    if not is_running:
        window.app_state.set_next_update_time("N/A")

def update_status_display(window, *args):
    """更新 AC 状态显示"""
    val = window.app_state.ac_status_val
    
    if val is True:
        status = "ON"
    elif val is False:
        status = "OFF"
    else:
        status = "N/A"
    
    window.status_label.setText(status)

def toggle_controller_loop(window):
    """切换控制器启动/停止"""
    # 临时禁用按钮，防止重复点击
    window.switch_button.setEnabled(False)
    
    try:
        if window.app_state.is_running_val:
            # 停止控制器
            window.stop_controller()
            window.app_state.set_running(False)
        else:
            # 启动控制器
            if not window.validate_interval():
                return
            window.start_controller()
            window.app_state.set_running(True)
    finally:
        # 恢复按钮
        window.switch_button.setEnabled(True)

def start_controller(window):
    """启动控制器线程"""
    if window.controller_thread and window.controller_thread.is_alive():
        window.log_message("Controller already running.")
        return
    
    window.stop_event = threading.Event()
    ctl = ACController(stop_event=window.stop_event, app_state=window.app_state)
    window.controller_thread = threading.Thread(
        target=ctl.control_loop,
        name="ACControllerThread",
        daemon=True
    )
    window.controller_thread.start()
    window.log_message("Controller started.")

def stop_controller(window):
    """停止控制器线程"""
    if window.stop_event:
        window.stop_event.set()
        window.log_message("Stopping controller...")
    window.stop_event = None
    window.controller_thread = None

def validate_interval(window) -> bool:
    """验证间隔时间是否有效"""
    try:
        if window.app_state.interval_minutes_val <= 0:
            raise ValueError
        return True
    except Exception:
        window.log_message("Error: Interval must be a positive integer (minutes).")
        return False

def process_log_queue(window):
    """处理日志队列（由定时器调用）"""
    try:
        while True:  # 一次性处理所有待处理日志
            message = window.log_queue.get_nowait()
            window.log_message(message)
    except queue.Empty:
        pass

def log_message(window, message: str):
    """在日志区域添加消息"""
    # PyQt6 的 QTextEdit 更简单，不需要手动管理 state
    window.log_area.append(message)
    
    # 自动滚动到底部
    scrollbar = window.log_area.verticalScrollBar()
    scrollbar.setValue(scrollbar.maximum())
