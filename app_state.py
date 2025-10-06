import tkinter as tk
from config import Config

"""
User configurable application state.
Dynamic UI variables.
"""
class AppState:
    """Holds UI-bound state.

    Interval统一以 *分钟* 存储 (IntVar)，需要秒的地方通过属性换算，
    避免各处 float/int/str 的重复来回转换。
    """

    def __init__(self):
        self.ac_status = tk.BooleanVar(value=None)
        self.token = tk.StringVar(value="")
        self.interval_minutes = tk.IntVar(value=Config.INTERVAL_MIN)
        self.next_check_time_str = tk.StringVar(value="N/A")
        self.is_running = tk.BooleanVar(value=False)

    @property
    def ac_status_val(self) -> bool:
        return self.ac_status.get()

    @property
    def token_val(self) -> str:
        return Config.TOKEN_PREFIX + self.token.get()

    @property
    def interval_minutes_val(self) -> int:
        return self.interval_minutes.get()

    @property
    def interval_seconds_val(self) -> int:
        return self.interval_minutes.get() * 60

    @property
    def next_update_time_val(self) -> str:
        return self.next_check_time_str.get()
    
    @property
    def is_running_val(self) -> bool:
        return self.is_running.get()

    # --- Public methods for other parts of the app to modify the state ---
    def set_status(self, status: bool):
        self.ac_status.set(status)

    def set_next_update_time(self, time_str: str):
        self.next_check_time_str.set(time_str)

    def set_running(self, is_running: bool):
        self.is_running.set(is_running)