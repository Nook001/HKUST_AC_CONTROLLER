import tkinter as tk

class AppState:
    def __init__(self):
        self.ac_status = tk.StringVar(value="Idle")
        self.next_check_time = tk.StringVar(value="N/A")
        self.is_running = tk.BooleanVar(value=False)

    @property
    def get_ac_status(self) -> tk.StringVar:
        """The variable for the AC status (for binding)."""
        return self.ac_status

    @property
    def get_next_update_time(self) -> tk.StringVar:
        """The variable for the next check time (for binding)."""
        return self.next_check_time
    
    @property
    def is_running_var(self) -> tk.BooleanVar:
        """The variable for the running state (for binding)."""
        return self.is_running

    # --- Public methods for other parts of the app to modify the state ---
    def set_status(self, status: str):
        """Sets the AC status (e.g., 'ON', 'OFF', 'Error')."""
        self.ac_status.set(status)

    def set_next_update_time(self, time_str: str):
        """Sets the time for the next check."""
        self.next_check_time.set(time_str)

    def set_running(self, is_running: bool):
        """Sets the running state of the controller."""
        self.is_running.set(is_running)

    def is_running(self) -> bool:
        """Returns the current running state."""
        return self.is_running.get()