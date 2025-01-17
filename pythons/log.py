import logging
import os
import datetime

logger = logging.getLogger("logs")
logger.setLevel(10)
fmt = "%(levelname)8s"
fmt2 = "%(asctime)s %(levelname)8s %(message)s"
class CustomFormatter(logging.Formatter):

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    white = '\x1b[38;5;255m'


    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: "%(asctime)s" + self.grey + self.fmt + self.reset + " %(message)s",
            logging.INFO: "%(asctime)s" + self.white + self.fmt + self.reset + " %(message)s",
            logging.WARNING: "%(asctime)s" + self.yellow + self.fmt + self.reset + " %(message)s",
            logging.ERROR: "%(asctime)s" + self.red + self.fmt + self.reset + " %(message)s",
            logging.CRITICAL: "%(asctime)s" + self.bold_red + self.fmt + self.reset + " %(message)s",
            
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt= datetime.datetime.now().astimezone().isoformat())
        return formatter.format(record)
    
console_handler = logging.StreamHandler()
console_handler.setLevel(10)
console_handler.setFormatter(CustomFormatter(fmt))
os.makedirs('/var/log/ids', exist_ok=True)
file_handler = logging.FileHandler("/var/log/ids/ids.log", mode="a", encoding="utf-8")
file_handler.setLevel(10)
file_handler.setFormatter(logging.Formatter(fmt2))

logger.addHandler(console_handler)
logger.addHandler(file_handler)