from utils.logger import logger

LINE = "=" * 60
SUB_LINE = "-" * 60


def section(title: str):
    print(f"\n{LINE}")
    print(title)
    print(LINE)
    logger.info(title)


def sub_section(title: str):
    print(f"\n{title}")
    print(SUB_LINE)
    logger.info(title)


def info(message: str):
    print(message)
    logger.info(message)


def success(message: str):
    print(f"✅ {message}")
    logger.info(message)


def error(message: str):
    print(f"❌ {message}")
    logger.error(message)