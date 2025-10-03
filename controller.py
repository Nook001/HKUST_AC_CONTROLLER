import requests
import logging
from datetime import datetime, timedelta
import threading
from config import Config
from app_state import AppState


class ACController:
	def __init__(self, stop_event: threading.Event, app_state: AppState):
		self.stop_event = stop_event
		self.app_state = app_state


	def update_ac_status(self) -> None:
		try:
			response = requests.get(Config.GET_URL, headers=Config.get_header(self.app_state.get_token), timeout=10)
			response.raise_for_status()
			data = response.json()
			ac_status = data['data']['ac_status']['DisconnectRelay']

			logging.info(f"✅ Fetched AC status: {"ON" if ac_status else "OFF"}.")
			logging.info(f"✅ 获取空调状态: {'开启' if ac_status else '关闭'}.")
			self.app_state.set_status(ac_status)

		except requests.exceptions.RequestException as e:
			logging.info(f"❌ Error fetching AC status: {e}")
			logging.info(f"❌ 获取空调状态时出错: {e}")
		except (KeyError, TypeError):
			logging.info("❌ Unexpected response format when fetching AC status.")
			logging.info("❌ 获取空调状态时响应格式异常.")


	def switch_ac(self) -> bool:
		try:
			# Send the toggle request
			response = requests.post(Config.POST_URL, headers=Config.post_header(self.app_state.get_token), data=Config.post_body(self.app_state.get_ac_status), timeout=10)
			response.raise_for_status()

			# Logging
			logging.info(f"✅ Request successful! Server response content: {response.json()['data']}")
			logging.info(f"✅ 请求成功! 服务器响应内容: {response.json()['data']}")
			return True

		except requests.exceptions.RequestException as e:
			logging.info("❌ Error toggling AC status: {e}")
			logging.info("❌ 切换空调状态时出错: {e}")
			return False


	def control_loop(self):
		while not self.stop_event.is_set():
			# Update status and toggle AC
			self.update_ac_status()
			self.switch_ac()

			next_action_time = datetime.now() + timedelta(seconds=self.app_state.get_interval)
			next_time_str = next_action_time.strftime('%H:%M:%S')
			self.app_state.set_next_update_time(next_time_str)

			# 使用 wait 代替 sleep，这样可以被 stop_event 立即中断
			self.stop_event.wait(self.app_state.get_interval)
