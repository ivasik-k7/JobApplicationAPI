import logging


class LoggerFactory:
    def __init__(
        self,
        log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    ):
        self.log_format = log_format
        self.level = level

    def create_logger(self, name, filename=None) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(self.level)

        formatter = logging.Formatter(self.log_format)

        if filename:
            file_handler = logging.FileHandler(filename)
            file_handler.setLevel(self.level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger
