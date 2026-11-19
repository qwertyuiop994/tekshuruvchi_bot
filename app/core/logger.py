import logging
import sys


def setup_logger(log_level: str = "INFO") -> logging.Logger:
    """
    Ilova uchun markazlashgan logger tizimini sozlaydi.
    """
    logger = logging.getLogger("SmartQuestionBot")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Agar handlerlar allaqachon mavjud bo'lsa, qayta qo'shmaymiz
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))

        # Format: Vaqt | Daraja | Modul | Xabar
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(module)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()
