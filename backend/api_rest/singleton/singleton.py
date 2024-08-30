import threading
from datetime import datetime


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RequestLogger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(RequestLogger, cls).__new__(
                        cls, *args, **kwargs
                    )
                    cls._instance._log = []
        return cls._instance

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._log.append(f"[{timestamp}] {message}")

    def get_log(self):
        return self._log

    def save_log_to_file(self, filename="request_log.txt"):
        with open(filename, "a") as file:
            for message in self._log:
                file.write(f"{message}\n")

    def clear_log(self):
        self._log = []
