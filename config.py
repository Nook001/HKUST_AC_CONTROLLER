import json


class Config:
	# 状态切换间隔，单位为秒
	INTERVAL_SECONDS = 1800

	TOKEN_PREFIX = "Bearer "

	# API 端点
	POST_URL = "https://w5.ab.ust.hk/njggt/api/app/prepaid/toggle-status"
	GET_URL = "https://w5.ab.ust.hk/njggt/api/app/prepaid/ac-status"

	@staticmethod
	def post_header(token: str):
		return {
			'Accept': 'application/json',
			'Accept-Encoding': 'gzip, deflate, br, zstd',
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
			'Authorization': token,
			'Connection': 'keep-alive',
			'Content-Type': 'application/json',
			'DNT': '1',
			'Host': 'w5.ab.ust.hk',
			'Origin': 'https://w5.ab.ust.hk',
			'Referer': 'https://w5.ab.ust.hk/njggt/app/home',
			'Sec-Fetch-Dest': 'empty',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Site': 'same-origin',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
			'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
			'sec-ch-ua-mobile': '?0',
			'sec-ch-ua-platform': '"Windows"'
		}


	@staticmethod
	def post_body(is_on: bool):
		return json.dumps({"toggle": {"status": 0 if is_on else 1}})


	@staticmethod
	def get_header(token: str):
		return {
			'Authorization': token,
			'Content-Type': 'application/json',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
		}

