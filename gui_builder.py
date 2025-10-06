import tkinter as tk
from tkinter import ttk, scrolledtext
from config import Config

def build_ui(app):
	build_root_container(app)
	build_token_section(app)
	build_interval_section(app)
	build_status_section(app)
	build_controls_section(app)
	build_log_section(app)

def build_root_container(app):
	app.main_frame = ttk.Frame(app, padding="10", style="App.TFrame")
	app.main_frame.pack(fill=tk.BOTH, expand=True)

def build_token_section(app):
	frame = ttk.Frame(app.main_frame, style="App.TFrame")
	frame.pack(fill=tk.X, pady=5)
	ttk.Label(frame, text=f"Token: {Config.TOKEN_PREFIX}", style="App.TLabel").pack(side=tk.LEFT)
	app.token_entry = ttk.Entry(frame, textvariable=app.app_state.token, width=50)
	app.token_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

def build_interval_section(app):
	frame = ttk.Frame(app.main_frame, style="App.TFrame")
	frame.pack(fill=tk.X, pady=5)
	ttk.Label(frame, text="Switch Interval:", style="App.TLabel").pack(side=tk.LEFT)
	app.interval_entry = ttk.Entry(frame, textvariable=app.app_state.interval_minutes, width=10)
	app.interval_entry.pack(side=tk.LEFT)

def build_status_section(app):
	"""
	两张独立圆角卡片：AC Status / Next Check
	使用淡蓝背景与圆角边框。
	"""
	container = ttk.Frame(app.main_frame, style="App.TFrame")
	container.pack(fill=tk.X, pady=8)

	style = app.style
	parent_bg = style.lookup("App.TFrame", "background") or "#F5F7FA"

	# 颜色配置
	card_bg = "#E8F2FE"  # 淡蓝背景
	border_color = "#C1D8F5"  # 边框浅蓝
	text_label_font = ("Segoe UI", 10, "bold")
	text_value_font = ("Segoe UI", 11)

	# 变量
	app.status_display_var = tk.StringVar()
	app.update_status_display()

	# 外层水平布局
	cards_frame = ttk.Frame(container, style="App.TFrame")
	cards_frame.pack(fill=tk.X)

	# 公共：绘制圆角矩形函数（使用 arc 外轮廓 + 矩形填充）
	def draw_round_rect(canvas, w, h, radius, fill, outline):
		canvas.delete("card-shape")
		r = radius
		if r * 2 > h:
			r = h // 2
		if r * 2 > w:
			r = w // 2
		
		# 1. 填充中央矩形与四条边矩形（组合成完整背景）
		canvas.create_rectangle(r, 0, w - r, h, fill=fill, outline="", tags="card-shape")
		canvas.create_rectangle(0, r, w, h - r, fill=fill, outline="", tags="card-shape")
		
		# 2. 四个角填充弧（pieslice 方式，但无 outline）
		canvas.create_arc(0, 0, 2 * r, 2 * r, start=90, extent=90,
						  style="pieslice", fill=fill, outline="", tags="card-shape")
		canvas.create_arc(w - 2 * r, 0, w, 2 * r, start=0, extent=90,
						  style="pieslice", fill=fill, outline="", tags="card-shape")
		canvas.create_arc(w - 2 * r, h - 2 * r, w, h, start=270, extent=90,
						  style="pieslice", fill=fill, outline="", tags="card-shape")
		canvas.create_arc(0, h - 2 * r, 2 * r, h, start=180, extent=90,
						  style="pieslice", fill=fill, outline="", tags="card-shape")
		
		# 3. 绘制边框（只用 arc 轮廓 + 直线连接四角）
		canvas.create_arc(0, 0, 2 * r, 2 * r, start=90, extent=90,
						  style="arc", outline=outline, width=1, tags="card-shape")
		canvas.create_arc(w - 2 * r, 0, w, 2 * r, start=0, extent=90,
						  style="arc", outline=outline, width=1, tags="card-shape")
		canvas.create_arc(w - 2 * r, h - 2 * r, w, h, start=270, extent=90,
						  style="arc", outline=outline, width=1, tags="card-shape")
		canvas.create_arc(0, h - 2 * r, 2 * r, h, start=180, extent=90,
						  style="arc", outline=outline, width=1, tags="card-shape")
		canvas.create_line(r, 0, w - r, 0, fill=outline, width=1, tags="card-shape")
		canvas.create_line(w, r, w, h - r, fill=outline, width=1, tags="card-shape")
		canvas.create_line(w - r, h, r, h, fill=outline, width=1, tags="card-shape")
		canvas.create_line(0, h - r, 0, r, fill=outline, width=1, tags="card-shape")

	# 创建通用卡片函数
	def create_card(parent, title, value_widget_builder):
		frame_holder = ttk.Frame(parent, style="App.TFrame")
		frame_holder.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=4)

		canvas = tk.Canvas(
			frame_holder,
			height=84,
			highlightthickness=0,
			bd=0,
			relief="flat",
			bg=parent_bg
		)
		canvas.pack(fill=tk.BOTH, expand=True)

		# 使用 tk.Frame 并设置背景色，使整个卡片内部都是淡蓝色
		inner_frame = tk.Frame(canvas, bg=card_bg)
		window_id = canvas.create_window(0, 0, anchor="nw", window=inner_frame, tags="inner")

		# 内容布局
		title_lbl = tk.Label(inner_frame, text=title, font=text_label_font, bg=card_bg, fg="#1E293B")
		title_lbl.grid(row=0, column=0, sticky="w", padx=14, pady=(14, 0))

		value_widget = value_widget_builder(inner_frame)
		value_widget.grid(row=1, column=0, sticky="w", padx=14, pady=(4, 14))

		inner_frame.grid_columnconfigure(0, weight=1)

		def on_resize(event):
			w = event.width
			h = event.height
			draw_round_rect(canvas, w, h, radius=30, fill=card_bg, outline=border_color)
			# 调整内部窗口位置与尺寸
			canvas.coords(window_id, 0, 0)
			canvas.itemconfig(window_id, width=w, height=h)

		canvas.bind("<Configure>", on_resize)
		return canvas

	# 构建两个卡片
	def build_status_value(parent):
		return tk.Label(parent, textvariable=app.status_display_var,
						font=text_value_font, bg=card_bg, fg="#1E293B")

	def build_next_check_value(parent):
		return tk.Label(parent, textvariable=app.app_state.next_check_time_str,
						font=text_value_font, bg=card_bg, fg="#1E293B")

	create_card(cards_frame, "AC Status", build_status_value)
	create_card(cards_frame, "Next Check", build_next_check_value)

def build_controls_section(app):
	app.switch_button = ttk.Button(
		app.main_frame,
		text="Start",
		style="Accent.TButton",
		command=app.toggle_controller_loop
	)
	app.switch_button.pack(fill=tk.X, pady=6)

def build_log_section(app):
	app.log_area = scrolledtext.ScrolledText(
		app.main_frame,
		wrap=tk.WORD,
		height=15,
		font=("Consolas", 10),
		background="#FFFFFF",
		borderwidth=1,
		relief="solid"
	)
	app.log_area.pack(fill=tk.BOTH, expand=True, pady=(4, 0))
	app.log_area.configure(state='disabled')