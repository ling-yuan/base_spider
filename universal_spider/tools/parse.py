import re
from typing import Any

from jsonpath_ng.ext import parse as jsonpath_parse
from lxml.html import etree
from scrapy import Selector


class JsonParser:
    default_value = []

    def parse(self, json_data: dict[str, Any] | list[Any], json_path: str, *args, **kwargs):
        """
        解析jsonpath 返回解析结果
        """
        parser = jsonpath_parse(json_path + "[*]")
        value_list = [match.value for match in parser.find(json_data)]
        return value_list if value_list else self.default_value


class RegexParser:
    default_value = []

    def parse(self, text: str | dict | list, regex: str, *args, **kwargs):
        """
        解析正则表达式 返回解析结果
        """
        if isinstance(text, (dict, list)):
            text = str(text)
        pattern = re.compile(regex, re.S)
        value_list = pattern.findall(text)
        return value_list if value_list else self.default_value


class XPathParser:
    default_value = []

    def parse(self, html: str, xpath: str, *args, **kwargs):
        """
        解析xpath 返回解析结果
        """
        value_list = []
        tree = etree.HTML(html, etree.HTMLParser())
        tmp_list = tree.xpath(xpath)
        for item in tmp_list:
            if isinstance(item, etree._Element):
                # 节点中的所有内容
                value_list.append(etree.tostring(item, encoding='utf-8').decode('utf-8').strip())  # type: ignore
            else:
                value_list.append(item)
        return value_list if value_list else self.default_value


class CssParser:
    default_value = []

    def parse(self, html: str, css_selector: str, *args, **kwargs):
        """
        解析css_selector 返回解析结果

        **暂时无法通过此方式解析出元素的属性或文本**
        """
        value_list = []
        sel = Selector(text=html)
        value_list = sel.css(css_selector).extract()
        return value_list if value_list else self.default_value
