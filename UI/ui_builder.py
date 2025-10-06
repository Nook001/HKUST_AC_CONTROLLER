from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QFrame
)
from PyQt6.QtCore import Qt
from config import Config

def build_ui(window):
    """构建整个 UI"""
    # 创建中央部件
    central_widget = QWidget()
    central_widget.setObjectName("MainWidget")
    window.setCentralWidget(central_widget)
    
    # 主布局
    window.main_layout = QVBoxLayout(central_widget)
    window.main_layout.setContentsMargins(10, 10, 10, 10)
    window.main_layout.setSpacing(10)
    
    # 构建各个部分
    build_token_section(window)
    build_interval_section(window)
    build_status_section(window)
    build_controls_section(window)
    build_log_section(window)

def build_token_section(window):
    """Token 输入区"""
    layout = QHBoxLayout()
    layout.setSpacing(10)
    
    # 标签
    label = QLabel(f"Token: {Config.TOKEN_PREFIX}")
    label.setMinimumWidth(80)
    
    # 输入框
    window.token_entry = QLineEdit()
    window.token_entry.setPlaceholderText("Enter your token here...")
    window.token_entry.setText(window.app_state.token)
    
    # 连接信号：输入框内容改变时更新状态
    window.token_entry.textChanged.connect(
        lambda text: setattr(window.app_state, 'token', text)
    )
    
    layout.addWidget(label)
    layout.addWidget(window.token_entry, stretch=1)
    
    window.main_layout.addLayout(layout)

def build_interval_section(window):
    """间隔时间输入区"""
    layout = QHBoxLayout()
    layout.setSpacing(10)
    
    # 标签
    label = QLabel("Switch Interval (minutes):")
    label.setMinimumWidth(150)
    
    # 输入框
    window.interval_entry = QLineEdit()
    window.interval_entry.setPlaceholderText("30")
    window.interval_entry.setText(str(window.app_state.interval_minutes))
    window.interval_entry.setMaximumWidth(100)
    
    # 连接信号
    def update_interval(text):
        try:
            value = int(text)
            if value > 0:
                window.app_state.interval_minutes = value
        except ValueError:
            pass
    
    window.interval_entry.textChanged.connect(update_interval)
    
    layout.addWidget(label)
    layout.addWidget(window.interval_entry)
    layout.addStretch()
    
    window.main_layout.addLayout(layout)

def build_status_section(window):
    """状态显示区 - 两张圆角卡片"""
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 10, 0, 10)
    layout.setSpacing(10)
    
    # 创建状态显示标签（需要在创建卡片之前）
    window.status_label = QLabel("N/A")
    window.status_label.setObjectName("CardValue")
    window.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    
    window.next_check_label = QLabel("N/A")
    window.next_check_label.setObjectName("CardValue")
    window.next_check_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    
    # AC Status 卡片
    ac_card = create_status_card("AC Status", window.status_label)
    layout.addWidget(ac_card, stretch=1)
    
    # Next Check 卡片
    next_card = create_status_card("Next Check", window.next_check_label)
    layout.addWidget(next_card, stretch=1)
    
    window.main_layout.addWidget(container)
    
    # 初始化状态显示
    window.update_status_display()

def create_status_card(title: str, value_widget: QLabel) -> QFrame:
    """创建单个状态卡片
    
    替代原来 150+ 行的 Canvas 绘制代码，使用 QFrame + QSS 实现圆角效果
    """
    card = QFrame()
    card.setObjectName("StatusCard")
    card.setMinimumHeight(84)
    
    # 卡片内部布局
    card_layout = QVBoxLayout(card)
    card_layout.setContentsMargins(14, 14, 14, 14)
    card_layout.setSpacing(4)
    
    # 标题标签
    title_label = QLabel(title)
    title_label.setObjectName("CardTitle")
    
    # 添加到布局
    card_layout.addWidget(title_label)
    card_layout.addWidget(value_widget)
    card_layout.addStretch()
    
    return card

def build_controls_section(window):
    """控制按钮区"""
    window.switch_button = QPushButton("Start")
    window.switch_button.setObjectName("StartButton")
    window.switch_button.setMinimumHeight(40)
    window.switch_button.clicked.connect(window.toggle_controller_loop)
    
    window.main_layout.addWidget(window.switch_button)

def build_log_section(window):
    """日志显示区"""
    window.log_area = QTextEdit()
    window.log_area.setObjectName("LogArea")
    window.log_area.setReadOnly(True)
    window.log_area.setMinimumHeight(200)
    
    # 设置等宽字体
    from PyQt6.QtGui import QFont
    font = QFont("Consolas", 10)
    font.setStyleHint(QFont.StyleHint.Monospace)
    window.log_area.setFont(font)
    
    window.main_layout.addWidget(window.log_area, stretch=1)
