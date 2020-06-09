import logging


class SwagUnknownException(Exception):
    pass


class Logger:
    logger_name = "SWAG"

    def __init__(self, name, make_logs):
        self.logger = logging.getLogger(Logger.logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.make_logs = make_logs
        self.name = name

        if self.make_logs:
            fh = logging.FileHandler("results/" + self.name + '/debug.log')
            fh.setLevel(logging.DEBUG)

            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message, exception):
        ex = exception if exception is not None else SwagUnknownException("Unknown exception")
        self.logger.error(message)
        self.logger.exception(exception, exc_info=True)

    def default(self, message):
        self.logger.info(message)
