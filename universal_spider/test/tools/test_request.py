import pytest
import scrapy
import scrapy.http
from universal_spider.tools.request import Request


def callback_example():
    pass


class TestRequest:

    def test_error_type(self):
        """
        测试请求类型错误
        """
        request_data = {
            "type": "html",
            "url": "https://127.0.0.1",
            "iteration_times": 1,
            "method": "get",
            "callback": callback_example,
        }
        try:
            req = Request(**request_data)
        except TypeError as e:
            assert str(e) == "Request Type must be 'api' or 'browser'"
        else:
            assert False

    def test_error_method(self):
        """
        测试请求类型错误
        """
        request_data = {
            "type": "api",
            "url": "https://127.0.0.1",
            "iteration_times": 1,
            "method": "put",
            "callback": callback_example,
        }
        try:
            req = Request(**request_data)
        except TypeError as e:
            assert str(e) == "Request Method must be 'get' or 'post'"
        else:
            assert False

    def test_api_get_form(self):
        """
        测试api请求，get方法，form参数
        """
        request_data = {
            "type": "api",
            "url": "https://127.0.0.1",
            "iteration_times": 1,
            "method": "get",
            "callback": callback_example,
            "form_params": {
                "key": "value",
            },
        }

        req = Request(**request_data)
        ans = scrapy.http.FormRequest(
            url="https://127.0.0.1",
            method="GET",
            formdata={"key": "value"},
            callback=callback_example,
            dont_filter=True,
        )
        assert req.__dict__ == ans.__dict__

    def test_api_post_form(self):
        """
        测试api请求，post方法，form参数
        """
        request_data = {
            "type": "api",
            "url": "https://127.0.0.1",
            "iteration_times": 1,
            "method": "post",
            "callback": callback_example,
            "form_params": {
                "key": "value",
            },
        }
        req = Request(**request_data)
        ans = scrapy.http.FormRequest(
            url="https://127.0.0.1",
            method="POST",
            formdata={"key": "value"},
            callback=callback_example,
            dont_filter=True,
        )
        assert req.__dict__ == ans.__dict__

    def test_api_get_json(self):
        """
        测试api请求，get方法，json参数
        """
        request_data = {
            "type": "api",
            "url": "https://127.0.0.1",
            "iteration_times": 1,
            "method": "get",
            "callback": callback_example,
            "json_params": {
                "key": "value",
            },
        }
        req = Request(**request_data)
        ans = scrapy.http.JsonRequest(
            url="https://127.0.0.1",
            method="GET",
            data={"key": "value"},
            callback=callback_example,
            dont_filter=True,
        )
        assert req.__dict__ == ans.__dict__

    def test_api_post_json(self):
        """
        测试api请求，post方法，form参数
        """
        request_data = {
            "type": "api",
            "url": "https://127.0.0.1",
            "iteration_times": 1,
            "method": "post",
            "callback": callback_example,
            "json_params": {
                "key": "value",
            },
        }
        req = Request(**request_data)
        ans = scrapy.http.JsonRequest(
            url="https://127.0.0.1",
            method="POST",
            data={"key": "value"},
            callback=callback_example,
            dont_filter=True,
        )
        assert req.__dict__ == ans.__dict__

    def test_api_get_query(self):
        """
        测试api请求，get方法，queryString参数
        """
        request_data = {
            "type": "api",
            "url": "https://127.0.0.1",
            "iteration_times": 1,
            "method": "get",
            "callback": callback_example,
            "query_params": {
                "key": "value",
            },
        }
        req = Request(**request_data)
        ans = scrapy.http.Request(
            url="https://127.0.0.1?key=value",
            method="GET",
            callback=callback_example,
            dont_filter=True,
        )
        assert req.__dict__ == ans.__dict__

    def test_api_post_query(self):
        """
        测试api请求，post方法，queryString参数
        """
        request_data = {
            "type": "api",
            "url": "https://127.0.0.1",
            "iteration_times": 1,
            "method": "post",
            "callback": callback_example,
            "query_params": {
                "key": "value",
            },
        }
        req = Request(**request_data)
        ans = scrapy.http.Request(
            url="https://127.0.0.1?key=value",
            method="POST",
            callback=callb