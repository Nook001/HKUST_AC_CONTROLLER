import threading
import queue
from controller import ACController

def init_logic(app):
    # 绑定逻辑函数为实例属性，供 UI / trace / 按钮调用
    app.update_ui_on_state_change = lambda *args: update_ui_on_state_change(app, *args)
    app.update_status_display = lambda *args: update_status_display(app, *args)
    app.toggle_controller_loop = lambda: toggle_controller_loop(app)
    app.start_controller = lambda: start_controller(app)
    app.stop_controller = lambda: stop_controller(app)
    app.validate_interval = lambda: validate_interval(app)
    app.process_log_queue = lambda: process_log_queue(app)
    app.log_message = lambda message: log_message(app, message)

def finalize_logic(app):
    """在 UI 构建完成后再绑定状态监听并启动日志轮询。"""
    app.app_state.is_running.trace_add("write", app.update_ui_on_state_change)
    app.app_state.ac_status.trace_add("write", app.update_status_display)
    app.process_log_queue()

def update_ui_on_state_change(app, *args):
    is_running = app.app_state.is_running_val
    app.switch_button.config(text="Stop" if is_running else "Start")
    app.token_entry.config(state="disabled" if is_running else "normal")
    app.interval_entry.config(state="disabled" if is_running else "normal")
    if not is_running:
        app.app_state.set_next_update_time("N/A")

def update_status_display(app, *args):
    val = app.app_state.ac_status_val
    if val is True:
        status = "ON"
    elif val is False:
        status = "OFF"
    else:
        status = "N/A"
    app.status_display_var.set(status)

def toggle_controller_loop(app):
    app.switch_button.config(state="disabled")
    try:
        if app.app_state.is_running_val:
            app.stop_controller()
            app.app_state.set_running(False)
        else:
            if not app.validate_interval():
                return
            app.start_controller()
            app.app_state.set_running(True)
    finally:
        app.switch_button.config(state="normal")

def start_controller(app):
    if app.controller_thread and app.controller_thread.is_alive():
        app.log_message("Controller already running.")
        return
    app.stop_event = threading.Event()
    ctl = ACController(stop_event=app.stop_event, app_state=app.app_state)
    app.controller_thread = threading.Thread(
        target=ctl.control_loop,
        name="ACControllerThread",
        daemon=True
    )
    app.controller_thread.start()
    app.log_message("Controller started.")

def stop_controller(app):
    if app.stop_event:
        app.stop_event.set()
        app.log_message("Stopping controller...")
    app.stop_event = None
    app.controller_thread = None

def validate_interval(app) -> bool:
    try:
        if app.app_state.interval_minutes_val <= 0:
            raise ValueError
        return True
    except Exception:
        app.log_message("Error: Interval must be a positive integer (minutes).")
        return False

def process_log_queue(app):
    try:
        message = app.log_queue.get_nowait()
        app.log_message(message)
    except queue.Empty:
        pass
    finally:
        app.after(100, app.process_log_queue)

def log_message(app, message: str):
    app.log_area.configure(state='normal')
    app.log_area.insert("end", message + "\n")
    app.log_area.see("end")
    app.log_area.configure(state='disabled')