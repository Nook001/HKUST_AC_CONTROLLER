import requests
import logging
from datetime import datetime, timedelta
import threading

from wakepy import keep
from config import Config
from state import AppState

logger = logging.getLogger(__name__)
class ACController:
	def __init__(self, stop_event: threading.Event, app_state: AppState):
		self.stop_event = stop_event
		self.app_state = app_state


	def update_ac_status(self) -> None:
		try:
			response = requests.get(Config.GET_URL, headers=Config.get_header(self.app_state.token_val), timeout=10)
			response.raise_for_status()
			data = response.json()
			ac_status = data['data']['ac_status']['DisconnectRelay']

			logger.info(f"✅ Fetched AC status: {"ON" if ac_status else "OFF"}.")
			logger.info(f"✅ 获取空调状态: {'开启' if ac_status else '关闭'}.")
			self.app_state.set_status(ac_status)

		except requests.exceptions.RequestException as e:
			logger.info(f"❌ Error fetching AC status: {e}")
			logger.info(f"❌ 获取空调状态时出错: {e}")
		except (KeyError, TypeError):
			logger.info("❌ Unexpected response format when fetching AC status.")
			logger.info("❌ 获取空调状态时响应格式异常.")


	def switch_ac(self) -> bool:
		try:
			# Send the toggle request
			response = requests.post(Config.POST_URL, headers=Config.post_header(self.app_state.token_val), data=Config.post_body(self.app_state.ac_status_val), timeout=10)
			response.raise_for_status()

			# Logging
			logger.info("✅ Request successful! Server response content:")
			logger.info("✅ 请求成功! 服务器响应内容:")
			logger.info(response.json()['data'])
			return True

		except requests.exceptions.RequestException as e:
			logger.info(f"❌ Error toggling AC status: {e}")
			logger.info(f"❌ 切换空调状态时出错: {e}")
			return False


	def control_loop(self):
		with keep.running():
			while not self.stop_event.is_set():
				# Update status and toggle AC
				self.update_ac_status()
				self.switch_ac()
				# Calculate and set next action time
				next_action_time = datetime.now() + timedelta(seconds=self.app_state.interval_seconds_val)
				next_time_str = next_action_time.strftime('%H:%M:%S')
				self.app_state.set_next_update_time(next_time_str)
				# Update status again to reflect new state
				self.update_ac_status()
				# 使用 wait 代替 sleep，这样可以被 stop_event 立即中断
				self.stop_event.wait(self.app_state.interval_seconds_val)
