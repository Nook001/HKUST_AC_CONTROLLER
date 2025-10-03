import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue
from main import ACController
from config import Config
import wakepy

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart AC Controller")
        self.geometry("600x500")


        # --- UI Elements ---
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Token Input
        token_frame = ttk.Frame(self.main_frame)
        token_frame.pack(fill=tk.X, pady=5)
        # Token Prefix
        ttk.Label(token_frame, text=f"Token:{Config.TOKEN_PREFIX}").pack(side=tk.LEFT)
        # Input Field
        self.token_value = tk.StringVar(value="")
        self.token_entry = ttk.Entry(token_frame, textvariable=self.token_value, width=50)
        self.token_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Interval Input
        interval_frame = ttk.Frame(self.main_frame)
        interval_frame.pack(fill=tk.X, pady=5)
        ttk.Label(interval_frame, text="Interval (minutes):").pack(side=tk.LEFT)
        self.interval_var = tk.StringVar(value=int(Config.INTERVAL_SECONDS / 60))
        self.interval_entry = ttk.Entry(interval_frame, textvariable=self.interval_var, width=10)
        self.interval_entry.pack(side=tk.LEFT)

        # Status Display
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, pady=10)
        self.ac_status = tk.StringVar(value="AC Status: Unknown")
        self.next_update_time = tk.StringVar(value="Next Switch: N/A")

        ttk.Label(status_frame, textvariable=self.ac_status, font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)
        ttk.Label(status_frame, textvariable=self.next_update_time, font=("Helvetica", 10)).pack(side=tk.RIGHT)

        # Start/Stop Button
        self.switch_button = ttk.Button(self.main_frame, text="Start", command=self.switch_button)
        self.switch_button.pack(fill=tk.X, pady=5)

        # Log Area
        self.log_area = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, height=15)
        self.log_area.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_area.configure(state='disabled')

        # --- Class variables ---
        self.controller_thread = None
        self.message_queue = queue.Queue()
        self.stop_event = None

        self.process_queue()

    # Switch Button handler
    def switch_button(self):
        is_running = self.controller_thread and self.controller_thread.is_alive()

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
            token = self.token_value.get()
            try:
                interval_minutes = int(self.interval_var.get())
                if interval_minutes <= 0:
                    raise ValueError
            except ValueError:
                self.log_message("Error: Interval must be a positive number.")
                return

            self.stop_event = threading.Event()
            controller = ACController(
                token=token,
                interval_seconds=interval_minutes * 60,
                message_queue=self.message_queue,
                stop_event=self.stop_event
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
