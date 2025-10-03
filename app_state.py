import tkinter as tk
from config import Config

"""
User configurable application state.
Dynamic UI variables.
"""
class AppState:
    def __init__(self):
        self.ac_status = tk.BooleanVar(value=False)
        self.token = tk.StringVar(value="")
        self.interval = tk.StringVar(value=str(Config.INTERVAL_SECONDS/60))
        self.next_check_time_str = tk.StringVar(value="N/A")
        self.is_running = tk.BooleanVar(value=False)

    @property
    def get_ac_status(self) -> bool:
        return self.ac_status.get()

    @property
    def get_token(self) -> str:
        return Config.TOKEN_PREFIX + self.token.get()

    @property
    def get_interval(self) -> str:
        return self.interval.get()

    @property
    def get_next_update_time(self) -> str:
        return self.next_check_time_str.get()
    
    @property
    def is_running_var(self) -> bool:
        return self.is_running.get()

    # --- Public methods for other parts of the app to modify the state ---
    def set_status(self, status: bool):
        self.ac_status.set(status)

    def set_next_update_time(self, time_str: str):
        self.next_check_time_str.set(time_str)

    def set_running(self, is_running: bool):
        self.is_running.set(is_running)

    def is_running(self) -> bool:
        return self.is_running.get()