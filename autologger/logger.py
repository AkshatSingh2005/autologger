import logging
import os
import sys


class PrintLoggerWriter:
    """
    File-like object that sends writes to a logger.
    """
    def __init__(self, logger, level=logging.INFO):
        self.logger = logger
        self.level = level

    def write(self, message):
        message = message.rstrip("\n")
        if not message:
            return
        self.logger.log(self.level, message)

    def flush(self):
        # For compatibility with file-like API
        pass


def setup_autologger(
    log_dir: str = "experiment/experiment_logs",
    log_file_name: str = "experiment_log.txt",
    logger_name: str = "experiment_logger",
    level: int = logging.INFO,
):
    """
    Set up a logger that also captures all print() output.
    Call this once at program start.
    """
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, log_file_name)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Avoid duplicate handlers
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Redirect print() / stdout to logger
    sys.stdout = PrintLoggerWriter(logger, level=level)
    # If you want stderr too:
    # sys.stderr = PrintLoggerWriter(logger, level=logging.ERROR)

    return logger
