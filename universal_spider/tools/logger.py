import logging
import colorlog


class logger(logging.Logger):

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        self.setLevel(level)
        # 创建控制台日志处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        # 定义颜色输出格式
        color_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s [%(name)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
        # 将颜色输出格式添加到控制台日志处理器
        console_handler.setFormatter(color_formatter)
        # 移除默认的handler
        for handler in self.handlers:
            self.removeHandler(handler)
        self.addHandler(console_handler)
