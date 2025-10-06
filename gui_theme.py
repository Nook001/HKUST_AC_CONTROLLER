import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

def init_theme(app):
    style = Style(theme="flatly")
    app.style = style  # 保存引用

    base_bg = "#F5F7FA"   # 页面底色（浅灰）
    card_bg = "#FFFFFF"   # 卡片白
    app.configure(background=base_bg)

    # 基础区域
    style.configure("App.TFrame", background=base_bg)
    style.configure("App.TLabel", background=base_bg)

    # 卡片
    style.configure("Card.TFrame", background=card_bg)
    style.configure("Card.TLabel", background=card_bg)

    # 强调按钮（保持主题主色，只加粗）
    style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=6)