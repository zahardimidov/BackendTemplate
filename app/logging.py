import logging

LOG_FORMAT_DEBUG = "%(pathname)s:%(levelname)s:%(message)s:%(funcName)s:%(lineno)d"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Создаем консольный обработчик
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Создаем форматтер и добавляем его в обработчик
formatter = logging.Formatter(LOG_FORMAT_DEBUG)
ch.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(ch)

