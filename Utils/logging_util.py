import logging
import queue
from logging.handlers import RotatingFileHandler

class QueueHandler(logging.Handler):
    """A custom handler to send logs to a queue for the GUI."""
    def __init__(self, log_queue: queue.Queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(self.format(record))

def setup_logging(gui_queue: queue.Queue):
    """
    Configures the root logger to send logs to a file and the GUI queue.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set the lowest level to capture

    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 1. File Handler to save logs to a file
    file_handler = RotatingFileHandler(
	    '../ac_controller.log', maxBytes=2 * 1024 * 1024, backupCount=2, encoding='utf-8'
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # 2. Queue Handler to send logs to the GUI
    queue_handler = QueueHandler(gui_queue)
    queue_handler.setFormatter(log_format)
    logger.addHandler(queue_handler)