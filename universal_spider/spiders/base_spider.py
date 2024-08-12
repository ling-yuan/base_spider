import ast
from copy import deepcopy
from functools import reduce
from typing import Any, Iterable
from aiostream.stream import list as alist
import scrapy
from scrapy.http.response import Response
from DrissionPage import ChromiumPage
from DrissionPage._pages.chromium_tab import ChromiumTab
from universal_spider.tools import *
from universal_spider.items import BaseItem


class BaseSpider(scrapy.Spider):
    name = "base_spider"

    stage_length = 0

    def __init__(self, *args, **kwargs: Any):
        # 调用父类的构造函数
        super(BaseSpider, self).__init__(*args, **kwargs)
        # 获取抓取配置
        _config = kwargs.get("config", {})
        # 转化格式
        self._config = ast.literal_eval(_config)
        # 类型检查
        if not isinstance(self.config, list):
            raise TypeError("config must be a list")
        # 初始化
        self.stage_length = len(self.config)
        logger("init").info(f"config: {self.config}")

    @property
    def config(self):
        """获取配置,防止被修改"""
        return deepcopy(self._config)

    def start_requests(self):
        """
        根据初始化时的配置，生成请求顺序中的第一个请求
        """
        # 若无配置，则返回
        if self.stage_length == 0:
            return None
        # 默认，从第一个阶段开始
        now_index = 0

        # 与_generate_request方法一致，由于本函数不允许异步，则复制至此处
        request_config = deepcopy(self.config[now_index]["request"])
        item = {}
        content: str = ""
        replacer = Replacer()
        config_fields = [
            "url",
            "type",
            "method",
            "headers",
            "iteration_times",
            "meta",
            "query_params",
            "json_params",
            "form_params",
        ]
        for config_field in config_fields:
            default_value = 1 if config_field == "iteration_times" else None if config_field == "url" else {}
            field_value = self._get_param_config(config_field, request_config, item, default_value)
            request_config[config_field] = field_value
        iteration_times = request_config.pop("iteration_times", 1)
        while iteration_times > 0:
            iteration_times -= 1
            new_item = deepcopy(item)
            request_config, new_request_config = replacer.replace(request_config, content, item=new_item)
            for one_of_config in new_request_config:
                yield Request(
                    **one_of_config,
                    callback=self.parse,
                    cb_kwargs={
                        "now_index": now_index,
                        "item": new_item,
                    },
                )

    def _get_param_config(self, config_name: str, request_config: dict, item: dict, default=None, *args, **kwargs):
        """
        根据请求配置和当前item，生成请求参数
        """
        ans = request_config.pop(config_name, default)
        ans = item.pop(f"next_{config_name}", ans)
        ans = ans[0] if isinstance(ans, list) else ans
        return ans

    async def _generate_request(self, index: int, item: dict, response="", *args, **kwargs):
        """
        根据请求配置和当前item，生成请求
        """
        # 深度拷贝请求参数和item
        request_config = deepcopy(self.config[index]["request"])
        item = deepcopy(item)
        # 获取上个阶段的内容
        content: str = await self._get_content(index - 1, response)
        # 定义替换器
        replacer = Replacer()
        # 获取配置
        config_fields = [
            "url",
            "type",
            "method",
            "headers",
            "iteration_times",
            "meta",
            "query_params",
            "json_params",
            "form_params",
        ]
        for config_field in config_fields:
            default_value = 1 if config_field == "iteration_times" else None if config_field == "url" else {}
            field_value = self._get_param_config(config_field, request_config, item, default_value)
            request_config[config_field] = field_value

        iteration_times = request_config.pop("iteration_times", 1)
        while iteration_times > 0:
            iteration_times -= 1
            new_item = deepcopy(item)
            request_config, new_request_config = replacer.replace(request_config, content, item=new_item)
            for one_of_config in new_request_config:
                yield Request(
                    **one_of_config,
                    callback=self.parse,
                    cb_kwargs={
                        "now_index": index,
                        "item": new_item,
                        "response_config": self.config[index]["response"],
                    },
                )

    async def parse(self, response: Response, **kwargs):
        """
        解析当前响应，发送解析结果或下一阶段请求
        """
        # 获取当前阶段索引
        now_index = kwargs["now_index"]
        # 获取上一阶段发送的item
        base_item = kwargs["item"]
        # 获取响应配置
        response_config = self.config[now_index]["response"]
        # 获取解析字段配置列表
        field_list = response_config.get("fields", [])
        # 获取当前响应的内容
        content = await self._get_content(now_index, response)
        # 基于base_item，生成新item列表（一个或多个）
        item_list = await self._update_item(
            now_index,
            base_item,
            field_list,
            response,
        )
        # 当前阶段处理完成
        now_index += 1
        # 若结束发送item
        if now_index >= self.stage_length:
            for item in item_list:
                save_fields = response_config.get("save_fields", None)
                if save_fields == None or save_fields == []:
                    yield self._gennerate_item(item)
                else:
                    tmp_item = {k: v for k, v in item.items() if k in save_fields}
                    yield self._gennerate_item(tmp_item)
            page: ChromiumPage = response.meta.get("page", None)
            if page:
                page.close()
            return

        # 循环每一项item
        for item in item_list:
            for req in await alist(self._generate_request(now_index, item, response)):
                yield req

        resp_type = self._response_type(now_index - 1)
        page: ChromiumPage = response.meta.get("page", None)
        if page:
            page.close()

    def _gennerate_item(self, item_dict, *args, **kwargs):
        item = BaseItem()
        for k, v in item_dict.items():
            if isinstance(v, dict):
                item[k] = v
            elif isinstance(v, list):
                if len(v) == 1:
                    item[k] = v[0]
                else:
                    item[k] = v
            else:
                item[k] = v
        return item

    async def _update_item(self, index: int, base_item: dict, field_list: list, response: Response, *args, **kwargs):
        """
        根据当前响应内容以及字段配置，基于原item，更新item
        """
        item_copy = base_item.copy()
        for field_config in field_list:
            value = await self._parse_field(
                index,
                response,
                field_config,
                item=deepcopy(base_item),
            )
            value = await self._process_value(value, response, field_config)
            value = value if value else field_config.get("default", "")
            save_length = field_config.get("save_length", 0)
            if save_length == 1 or save_length == "1":
                value = reduce(lambda x, y: x + y, value)
                value = [value]
            elif save_length == 0 or save_length == "0":
                pass
            else:
                logger(self.__class__.__name__).error(f"save_length must be 0 or 1, got {save_length}")
                raise ValueError(f"save_length must be 0 or 1, got {save_length}")
            if field_config["name"] not in base_item.keys():
                item_copy[field_config["name"]] = value
            else:
                if field_config.get("save_method", "") == "replace":
                    item_copy[field_config["name"]] = value
                elif field_config.get("save_method", "") == "append":
                    item_copy[field_config["name"]] += value
                else:
                    item_copy[field_config["name"]] = value

        item_list = []
        max_len = max([len(value) for value in item_copy.values() if isinstance(value, Iterable)])
        for k in item_copy.keys():
            if len(item_copy[k]) == 1:
                item_copy[k] *= max_len
            elif len(item_copy[k]) != max_len:
                raise Exception(f"字段 {k} 的长度不一致")
        item_list = [{k: [value[i]] for k, value in item_copy.items()} for i in range(max_len)]
        return item_list

    async def _parse_field(self, index: int, response: Response, field_config: dict, *args, **kwargs):
        """
        根据单个字段配置，解析并返回结果
        """
        resp_type = self._response_type(index)
        if resp_type == "browser":
            replacer = BrowserReplacer()
            _, new_value = replacer.replace(field_config["value"], response.meta["page"], *args, **kwargs)
        else:
            data = await self._get_content(index, response)
            replacer = Replacer()
            _, new_value = replacer.replace(field_config["value"], data, *args, **kwargs)
        return new_value

    async def _process_value(self, value, response: Response, field_config: dict, *args, **kwargs):
        """
        根据解析后的值，进行后续处理
        """
        process_function = ProcessFunction()
        process_list = field_config.get("after_process", [])
        for process_config in process_list:
            func_name = process_config.get("name", "")
            func_args = process_config.get("args", "")
            if func_name:
                value = process_function.process_value(value, func_name, func_args)
        return value

    def _response_type(self, index: int):
        """
        获取响应类型
        """
        request_config = self.config[index]["request"]
        response_config = self.config[index]["response"]
        resp_type = "browser" if request_config["type"] == "browser" else response_config.get("type", "html")
        return resp_type

    async def _get_content(self, index: int, response: Response | None = None):
        """
        根据请求配置，获取响应内容
        """
        resp_type = self._response_type(index)
        if not response:
            return ""
        if resp_type == "browser":
            return response.meta["page"].html
        return response.text if resp_type == "html" else response.json()
