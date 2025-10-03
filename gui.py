import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue

from app_state import AppState
from controller import ACController
from config import Config
import wakepy

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart AC Controller")
        self.geometry("600x500")
        self.app_state = AppState()

        # --- Class variables ---
        self.controller_thread = None
        self.message_queue = queue.Queue()
        self.stop_event = None

        self.controller = ACController(self.stop_event, self.app_state)


        # --- UI Elements ---
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)


        # Token Input
        # Frame
        token_frame = ttk.Frame(self.main_frame)
        token_frame.pack(fill=tk.X, pady=5)
        # Token Prefix
        ttk.Label(token_frame, text=f"Token:{Config.TOKEN_PREFIX}").pack(side=tk.LEFT)
        # Input Field
        self.token_entry = ttk.Entry(token_frame, textvariable=self.app_state.token, width=50)
        self.token_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)


        # Interval Input
        # Frame
        interval_frame = ttk.Frame(self.main_frame)
        interval_frame.pack(fill=tk.X, pady=5)
        # Interval Prefix
        ttk.Label(interval_frame, text="Switch Interval:").pack(side=tk.LEFT)
        # Input Field
        self.interval_entry = ttk.Entry(interval_frame, textvariable=self.app_state.interval, width=10)
        self.interval_entry.pack(side=tk.LEFT)


        # AC Status Display
        # Frame
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, pady=10)

        ttk.Label(status_frame, text="Current AC Status:", font=("Helvetica", 12)).pack(side=tk.LEFT)
        #
        ttk.Label(status_frame, textvariable=self.app_state.ac_status, font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)
        ttk.Label(status_frame, textvariable=self.app_state.next_check_time_str, font=("Helvetica", 10)).pack(side=tk.RIGHT)
        ttk.Label(status_frame, text="Next Check:", font=("Helvetica", 10)).pack(side=tk.RIGHT)

        # Start/Stop Button
        self.switch_button = ttk.Button(self.main_frame, text="Start", command=self.switch_button)
        self.switch_button.pack(fill=tk.X, pady=5)

        # Log Area
        self.log_area = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, height=15)
        self.log_area.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_area.configure(state='disabled')

        self.process_queue()

    # Switch Button handler
    def switch_button(self):
        is_running = self.controller_thread and self.controller_thread.is_alive()

        # If running, stop it; if not, start it
        if is_running:
            # Stop the loop
            if self.stop_event:
                self.stop_event.set()
            # Update button text
            self.switch_button.config(text="Start")
            # Unlock input fields
            self.token_entry.config(state="normal")
            self.interval_entry.config(state="normal")
        else:
            # Start the loop
            try:
                interval_minutes = int(self.interval_var.get())
                if interval_minutes <= 0:
                    raise ValueError
            except ValueError:
                self.log_message("Error: Interval must be a positive number.")
                return

            self.stop_event = threading.Event()
            controller = ACController(
                stop_event=self.stop_event,
                app_state=self.app_state
            )

            self.controller_thread = threading.Thread(target=controller.control_loop, daemon=True)
            self.controller_thread.start()

            self.switch_button.config(text="Stop")
            self.token_entry.config(state="disabled")
            self.interval_entry.config(state="disabled")
            self.next_update_time.set("Next Switch: N/A")

    def process_queue(self):
        try:
            message = self.message_queue.get_nowait()
            if message.startswith("STATUS:"):
                status = message.split(":", 1)[1]
                self.ac_status.set(f"AC Status: {status}")
                if status in ["Stopped", "Error", "Idle"]:
                     self.next_update_time.set("Next Check: --:--:--")
            elif message.startswith("NEXT_CHECK:"):
                time_str = message.split(":", 1)[1]
                self.next_update_time.set(f"Next Check: {time_str}")
            else:
                self.log_message(message)
        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_queue)

    def log_message(self, message):
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, message + '\n')
        self.log_area.see(tk.END) # Auto-scroll
        self.log_area.configure(state='disabled')


if __name__ == "__main__":
    app = App()
    app.mainloop()
