import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue

from app_state import AppState
from controller import ACController
from config import Config
from logging_util import setup_logging

class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Smart AC Controller")
		self.geometry("600x500")
		# --- Class variables ---
		self.app_state = AppState()
		self.controller_thread = None
		self.stop_event = None
		self.log_queue = queue.Queue() # 3. 创建日志队列
		setup_logging(self.log_queue) # 4. 初始化日志系统


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


		# Status Display
		# Frame
		status_frame = ttk.Frame(self.main_frame)
		status_frame.pack(fill=tk.X, pady=10)
		# AC Status
		self.status_display_var = tk.StringVar()
		self.update_status_display() # 初始化
		self.app_state.ac_status.trace_add("write", self.update_status_display) # 绑定更新事件
		ttk.Label(status_frame, text="Current Status:", font=("Helvetica", 12)).pack(side=tk.LEFT)
		ttk.Label(status_frame, textvariable=self.status_display_var, font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)
		# Next Check Time
		ttk.Label(status_frame, textvariable=self.app_state.next_check_time_str, font=("Helvetica", 10)).pack(side=tk.RIGHT)
		ttk.Label(status_frame, text="Next Check:", font=("Helvetica", 10)).pack(side=tk.RIGHT)


		# Start/Stop Button
		self.switch_button = ttk.Button(self.main_frame, text="Start", command=self.toggle_controller)
		self.switch_button.pack(fill=tk.X, pady=5)

		# Log Area
		self.log_area = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, height=15)
		self.log_area.pack(fill=tk.BOTH, expand=True, pady=5)
		self.log_area.configure(state='disabled')
		self.process_log_queue()

		self.app_state.is_running.trace_add("write", self.update_ui_on_state_change)


	def update_ui_on_state_change(self, *args):
		"""当 is_running 状态改变时，自动更新UI"""
		is_running = self.app_state.get_is_running
		if is_running:
			self.switch_button.config(text="Stop")
			self.token_entry.config(state="disabled")
			self.interval_entry.config(state="disabled")
		else:
			self.switch_button.config(text="Start")
			self.token_entry.config(state="normal")
			self.interval_entry.config(state="normal")

	def update_status_display(self, *args):
		"""Callback to update status label text."""
		match self.app_state.get_ac_status:
			case True: status = "ON"
			case False: status = "OFF"
			case _: status = "N/A"
		self.status_display_var.set(status)

	# Switch Button handler
	def toggle_controller(self):
		# If running, stop it
		if self.app_state.get_is_running:
			# Stop Signal
			if self.stop_event:
				self.stop_event.set()
		# If not, start it
		else:
			# Start the loop
			try:
				interval_minutes = int(self.app_state.get_interval)
				if interval_minutes <= 0: raise ValueError
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
		self.app_state.set_running(not self.app_state.get_is_running)


	def process_log_queue(self): # 6. 恢复这个方法
		"""Checks the log queue and displays messages in the GUI."""
		try:
			message = self.log_queue.get_nowait()
			self.log_message(message)
		except queue.Empty:
			pass
		finally:
			self.after(100, self.process_log_queue)

	def log_message(self, message):
		self.log_area.configure(state='normal')
		self.log_area.insert(tk.END, message + '\n')
		self.log_area.see(tk.END) # Auto-scroll
		self.log_area.configure(state='disabled')


if __name__ == "__main__":
	app = App()
	app.mainloop()
