from functools import reduce
import inspect
import time
from universal_spider.tools.parse import JsonParser
from universal_spider.tools.parse import XPathParser
from universal_spider.tools.parse import RegexParser
from universal_spider.tools.parse import CssParser


class Function:
    """
    函数类

    **所有函数返回类型均为列表**
    """

    def __init__(self) -> None:
        # 类中的函数字典
        self.function_dict = {}
        # 注册
        for name, func in inspect.getmembers(self, inspect.ismethod or inspect.isfunction):
            self.function_dict[name] = func

        # add方法所需变量
        self.add_now_num = 0
        self.add_used_times = 0

    def add(self, func_params, *args, **kwargs):
        """递增函数，用于生成递增的数字"""
        func_params = func_params.split(",")
        func_params = [int(i) for i in func_params]
        l = len(func_params)
        if l < 1 or l > 2:
            raise Exception("function: add params error")
        elif l == 1:
            func_params.append(1)
        sum = reduce(lambda x, y: x + y, [int(i) for i in func_params])
        next_func_params = [str(sum)]
        if l > 1:
            next_func_params.append(str(func_params[1]))
        next_func_content = ",".join(next_func_params)
        return next_func_content, [str(func_params[0])]

    def now_timestamp(self, func_params="", *args, **kwargs):
        '''获取当前时间戳'''
        return func_params, [str(int(time.time()))]

    def parse_jsonpath(self, data, jsonpath, *args, **kwargs):
        '''解析jsonpath'''
        json_parser = JsonParser()
        return json_parser.parse(data, jsonpath)

    def parse_xpath(self, data, xpath, *args, **kwargs):
        '''解析xpath'''
        xpath_parser = XPathParser()
        return xpath_parser.parse(data, xpath)

    def parse_regex(self, data, regex, *args, **kwargs):
        '''解析正则'''
        regex_parser = RegexParser()
        return regex_parser.parse(data, regex)

    def parse_css(self, data, css, *args, **kwargs):
        '''解析css'''
        css_parser = CssParser()
        return css_parser.parse(data, css)
