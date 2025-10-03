import requests
import json
import logging

from datetime import datetime, timedelta
import threading

import app_state
from config import Config
from app_state import AppState


class ACController:
	def __init__(self, token: str, interval_seconds: int, stop_event: threading.Event, app_state: AppState):
		self.token = f"Bearer {token}"
		self.interval_seconds = interval_seconds
		self.stop_event = stop_event
		self.app_state = app_state


	def get_ac_status(self) -> None:
		try:
			response = requests.get(Config.GET_URL, headers=Config.get_header(self.token), timeout=10)
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

	def switch_ac(self, is_on: bool) -> bool:
		try:
			action_text = 'OFF' if is_on else 'ON'
			self.log(f"🚀 Sending request to switch AC {action_text}...")
			self.log(f"🚀 正在发送请求, 切换空调状态为: {action_text}...")

			response = requests.post(
				Config.POST_URL,
				headers=Config.post_header(self.token),
				data=json.dumps({"toggle": {"status": 0 if is_on else 1}}),
				timeout=10
			)
			response.raise_for_status()

			self.log("✅ Request successful!")
			self.log(f"Server response content: {response.json()['data']}")
			self.log("✅ 请求成功!")
			self.log(f"服务器响应内容: {response.json()['data']}\n")
			return True

		except requests.exceptions.RequestException as e:
			self.log(f"❌ 请求失败: {e}\n")
			return False

	def control_loop(self):
		self.log("❄️ Smart AC Control thread started.")
		self.log(f"    - Checking status and toggling every {self.interval_seconds / 60} minutes.")

		while not self.stop_event.is_set():
			is_on = self.get_ac_status()

			if is_on is None:
				self.log("Skipping this cycle due to an error fetching status.")
				self.log("由于获取状态时出错，跳过本次循环。")
			else:
				self.switch_ac(is_on)

			next_action_time = datetime.now() + timedelta(seconds=self.interval_seconds)
			next_time_str = next_action_time.strftime('%H:%M:%S')

			self.log(f"💤 Sleeping. Next check at {next_time_str}.")
			self.log(f"💤 休眠中. 下次检查时间: {next_time_str}.\n")
			self.queue.put(f"NEXT_CHECK:{next_time_str}")

			# 使用 wait 代替 sleep，这样可以被 stop_event 立即中断
			self.stop_event.wait(self.interval_seconds)

		self.log("🛑 AC Control thread stopped.")
		self.queue.put("STATUS:Stopped")
