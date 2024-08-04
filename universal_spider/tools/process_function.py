from copy import deepcopy
from functools import reduce
import inspect
import re
from lxml import etree
from universal_spider.tools import logger
from universal_spider.tools.wapper import catch_wapper, deepcopy_wapper


class ProcessFunction(object):
    """
    用于解析字段所有前的额外处理，或某个字段前后的额外处理
    """

    def __init__(self, resp=None, *args, **kwargs):
        self.resp = resp
        # 类中的函数字典
        self.function_dict = {}
        # 注册
        for name, func in inspect.getmembers(self, inspect.ismethod or inspect.isfunction):
            self.function_dict[name] = func

    @catch_wapper
    def browser_sleep(self, data, func_params: str, *args, **kwargs):
        """
        browser: 等待
        """
        pass

    @catch_wapper
    def browser_click(self, data, func_params: str, *args, **kwargs):
        """
        browser: 点击
        """
        pass

    @catch_wapper
    def browser_scroll(self, data, func_params: str, *args, **kwargs):
        """
        browser: 滚动界面
        """
        pass

    @catch_wapper
    def browser_input(self, data, func_params: str, *args, **kwargs):
        """
        browser: 输入
        """
        pass

    @catch_wapper
    def browser_execute(self, data, func_params: str, *args, **kwargs):
        """
        browser: 执行js
        """
        pass

    @catch_wapper
    def str_remove_by_regex(self, data, func_params: str, *args, **kwargs):
        """
        string: 正则删除
        """
        if isinstance(data, list):
            data = deepcopy(data)
            for i in range(len(data)):
                data[i] = self.str_remove_by_regex(data[i], func_params)
            return data
        elif isinstance(data, str):
            pattern = re.compile(func_params)
            return pattern.sub("", data)
        else:
            logger("str_remove_by_regex").warning("the type of data is not str or list")
            return data

    @catch_wapper
    def str_replace_by_regex(self, data, func_params: str, *args, **kwargs):
        """
        string: 正则替换
        """
        if isinstance(data, list):
            data = deepcopy(data)
            for i in range(len(data)):
                data[i] = self.str_replace_by_regex(data[i], func_params)
            return data
        elif isinstance(data, str):
            params = func_params.split(",")
            pattern = re.compile(params[0])
            return pattern.sub(params[1], data)
        else:
            logger("str_replace_by_regex").warning("the type of data is not str or list")
            return data

    @catch_wapper
    def str_extract_by_regex(self, data, func_params: str, *args, **kwargs):
        """
        string: 正则提取
        """
        if isinstance(data, list):
            data = deepcopy(data)
            for i in range(len(data)):
                data[i] = self.str_extract_by_regex(data[i], func_params)
            return data
        elif isinstance(data, str):
            params = func_params.split(",")
            value_list = []
            for i in params:
                value_list.extend(reduce(lambda x, y: x + y, re.findall(i, data)))
            return reduce(lambda x, y: x + y, value_list)
        else:
            logger("str_extract_by_regex").warning("the type of data is not str or list")
            return data

    @catch_wapper
    def html_removetag_by_xpath(self, data, func_params: str, *args, **kwargs):
        """
        html: xpath删除标签
        """
        if isinstance(data, list):
            data = deepcopy(data)
            for i in range(len(data)):
                data[i] = self.html_removetag_by_xpath(data[i], func_params)
            return data
        elif isinstance(data, str):
            tree = etree.HTML(data, parser=etree.HTMLParser(encoding="utf-8"))
            for i in tree.xpath(func_params):
                i.getparent().remove(i)
            return etree.tostring(tree, encoding="utf-8").decode()
        else:
            logger("html_removetag_by_xpath").warning("the type of data is not str or list")
            return data

    @catch_wapper
    def html_removestyle_by_xpath(self, data, func_params: str, *args, **kwargs):
        """
        html: xpath删除style
        """
        if isinstance(data, list):
            data = deepcopy(data)
            for i in range(len(data)):
                data[i] = self.html_removestyle_by_xpath(data[i], func_params)
            return data
        elif isinstance(data, str):
            tree = etree.HTML(data, parser=etree.HTMLParser(encoding="utf-8"))
            for i in tree.xpath(func_params):
                if "style" in i.attrib:
                    i.attrib.pop("style")
            return etree.tostring(tree, encoding="utf-8").decode()
        else:
            logger("html_removestyle_by_xpath").warning("the type of data is not str or list")
            return data

    @catch_wapper
    def html_replacetag_by_xpath(self, data, func_params: str, *args, **kwargs):
        """
        html: xpath替换标签
        """
        if isinstance(data, list):
            data = deepcopy(data)
            for i in range(len(data)):
                data[i] = self.html_replacetag_by_xpath(data[i], func_params)
            return data
        elif isinstance(data, str):
            func_params = func_params.split(",")
            xpath = func_params[0]
            tag = func_params[1]
            tree = etree.HTML(data)
            for i in tree.xpath(xpath):
                i.tag = tag
            return etree.tostring(tree, encoding="utf-8").decode()
        else:
            logger("html_replacetag_by_xpath").warning("the type of data is not str or list")
            return data

    def format_value(self, data, func_params: str, *args, **kwargs):
        """
        格式化数据
        """
        if isinstance(data, list):
            data = deepcopy(data)
            for i in range(len(data)):
                data[i] = self.format_value(data[i], func_params)
            return data
        elif isinstance(data, str):
            return func_params.format(data)
        else:
            logger("format_value").warning("the type of data is not str or list")
            return data
