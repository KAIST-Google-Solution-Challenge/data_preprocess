# 로그 생성
import logging
from colorlog import ColoredFormatter

def getLogger():
    logger = logging.getLogger()
    logger.handlers = []       # No duplicated handlers
    logger.propagate = False   # workaround for duplicated logs in ipython

    # 로그의 출력 기준 설정
    logger.setLevel(logging.DEBUG)

    # log 출력 형식
    # formatter = logging.Formatter('\033[92m[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s\033[0m')
    formatter = ColoredFormatter(
        # "%(log_color)s[%(asctime)s] %(message)s",
        '%(log_color)s [%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s',
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'blue',
            'INFO':     'white,bold',
            'INFOV':    'cyan,bold',
            'WARNING':  'yellow',
            'ERROR':    'red,bold',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    # log 출력
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    return logger;