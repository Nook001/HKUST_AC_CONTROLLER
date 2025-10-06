import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue

from state import AppState
from logging_util import setup_logging
from gui_builder import build_ui
from gui_handler import init_logic, finalize_logic
from gui_theme import init_theme

class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Smart AC Controller")
		self.geometry("600x500")

		# --- State / threading ---
		self.app_state = AppState()
		self.controller_thread = None
		self.stop_event = None
		self.log_queue = queue.Queue()
		setup_logging(self.log_queue)

		# 主题初始化（必须先于 build_ui）
		init_theme(self)

		# 绑定逻辑函数为实例属性，供 UI / trace / 按钮调用
		init_logic(self)

		# --- Build UI (分块函数) ---
		build_ui(self)

		# 绑定状态变更回调
		finalize_logic(self)

if __name__ == "__main__":
	app = App()
	app.mainloop()