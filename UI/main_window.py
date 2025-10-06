import sys
import queue
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer

from Controller.app_state import AppState
from Utils.logging_util import setup_logging
from UI.ui_builder import build_ui
from UI.ui_handler import init_logic, finalize_logic

class MainWindow(QMainWindow):
	"""主窗口类 - 使用 PyQt6"""

	def __init__(self):
		super().__init__()
		# 窗口基本设置
		self.setWindowTitle("Smart AC Controller")
		self.setGeometry(100, 100, 600, 550)

		# --- State / threading ---
		self.app_state = AppState()
		self.controller_thread = None
		self.stop_event = None
		self.log_queue = queue.Queue()

		# 设置日志系统
		setup_logging(self.log_queue)

		# 绑定逻辑函数为实例属性（在 build_ui 之前）
		init_logic(self)

		# --- Build UI (分块函数) ---
		build_ui(self)

		# 加载样式表
		self.load_stylesheet()

		# 绑定状态变更回调（在 UI 构建完成后）
		finalize_logic(self)

		# 启动日志队列处理定时器（替代 Tkinter 的 after()）
		self.log_timer = QTimer(self)
		self.log_timer.timeout.connect(self.process_log_queue)
		self.log_timer.start(100)  # 每 100ms 检查一次

	def load_stylesheet(self):
		import os
		style_path = os.path.join(os.path.dirname(__file__), 'styles.qss')
		"""加载 QSS 样式表"""
		with open(style_path, 'r', encoding='utf-8') as f:
			self.setStyleSheet(f.read())


def main():
	"""应用程序入口"""
	app = QApplication(sys.argv)

	# 设置应用程序字体
	app.setStyle('Fusion')  # 使用 Fusion 风格，跨平台一致

	window = MainWindow()
	window.show()

	sys.exit(app.exec())

if __name__ == "__main__":
	main()
