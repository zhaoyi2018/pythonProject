# -*- coding: utf-8 -*-
# @Time    : 6/22/21 3:37 PM
# @Author  : Bian Binbin
# @FileName: logger.py
import logging
import os
import sys
import time


class Logger:
    def __init__(
            self,
            name=os.path.split(os.path.splitext(sys.argv[0])[0])[-1],
            set_level="debug",
            console=True,
            # formatter=logging.Formatter(fmt='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s', datefmt='%Y/%m/%d %H:%M:%S'),
            formatter=logging.Formatter(fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S'),
            file_name=None,
            # file_name=time.strftime("%Y-%m-%d.log", time.localtime()),
            file_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "log"),
    ):
        '''
            set_level? ?????????????DEBUG
            name? ????????name?????????name
            file_name? ?????????????????-?-?.log?
            file_path? ????????????logger.py??????log???
            console? ????????????True
        '''
        # print('test..')
        self.logger = logging.getLogger(name)

        if set_level.lower() == "critical":
            self.logger.setLevel(logging.CRITICAL)
        elif set_level.lower() == "error":
            self.logger.setLevel(logging.ERROR)
        elif set_level.lower() == "warning":
            self.logger.setLevel(logging.WARNING)
        elif set_level.lower() == "info":
            self.logger.setLevel(logging.INFO)
        elif set_level.lower() == "debug":
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.NOTSET)

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # log_file_path = os.path.join(file_path, file_name)
        # log_handler = logging.FileHandler(log_file_path)
        # log_handler.setFormatter(formatter)
        # self.logger.addHandler(log_handler)

        if file_name:
            log_file_path = os.path.join(file_path, file_name)
            log_handler = logging.FileHandler(log_file_path+".log")
            log_handler.setFormatter(formatter)
            self.logger.addHandler(log_handler)

        if console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def addHandler(self, hdlr):
        self.logger.addHandler(hdlr)

    def removeHandler(self, hdlr):
        self.logger.removeHandler(hdlr)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)


if __name__ == '__main__':
    logger = Logger()
    logger.info("ssssssss???")

    try:
        result = 10 / 0
    except Exception:
        logger.error('Faild to get result', exc_info=True)
    logger.debug('Finished')