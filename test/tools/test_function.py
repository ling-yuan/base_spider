import sys_path
import pytest
from universal_spider.tools.function import Function


class TestFunction(object):

    @pytest.fixture
    def function(self):
        return Function()

    @pytest.fixture
    def jsondata(self):
        return {
            "str": "string",
            "list": [1, 2, 3],
            "dict": {"key": "value"},
            "list_dict": [
                {"key": "value1"},
                {"key": "value2"},
            ],
        }

    @pytest.fixture
    def htmldata(self):
        return """
        <body>
            <table>
                <tr>
                    <th>编号</th>
                    <th>姓名</th>
                    <th>电话</th>
                    <th>检测结果</th>
                    <th>检测时间</th>
                </tr>
            </table>
            <button onclick="select()">查询</button>
            <script type="text/javascript" src="js/yezhu.js"></script>
        </body>
        """

    def test_function_dict(self, function):
        """
        测试function_dict, 是否自动注册函数到字典中
        """
        assert function.function_dict == {
            "__init__": function.__init__,
            "add": function.add,
            "now_timestamp": function.now_timestamp,
            "parse_jsonpath": function.parse_jsonpath,
            "parse_xpath": function.parse_xpath,
            "parse_regex": function.parse_regex,
            "parse_css": function.parse_css,
        }

    def test_add(self, function):
        """
        测试add函数
        """
        assert function.add("1,2") == ("3,2", ["1"])
        assert function.add("3,2") == ("5,2", ["3"])
        assert function.add("4") == ("5", ["4"])

    def test_now_timestamp(self, function):
        """
        测试now_timestamp函数
        """
        pass

    def test_parse_jsonpath(self, function: Function, jsondata, htmldata):
        """
        测试parse_jsonpath函数
        """
        jsonpath = "$.str"
        assert function.parse_jsonpath(jsondata, jsonpath) == ["string"]
        jsonpath = "$.list"
        assert function.parse_jsonpath(jsondata, jsonpath) == [1, 2, 3]
        jsonpath = "$.dict.key"
        assert function.parse_jsonpath(jsondata, jsonpath) == ["value"]
        jsonpath = "$.list_dict[*].key"
        assert function.parse_jsonpath(jsondata, jsonpath) == ["value1", "value2"]
        jsonpath = "$.list_dict..key"
        assert function.parse_jsonpath(jsondata, jsonpath) == ["value1", "value2"]
        jsonpath = "$.error"
        assert function.parse_jsonpath(jsondata, jsonpath) == []

        try:
            jsonpath = "$.error"
            ans = function.parse_jsonpath(htmldata, "$.error")
            assert False
        except Exception as e:
            assert True

    def test_parse_xpath(self, function: Function, htmldata, jsondata):
        """
        测试parse_xpath函数
        """
        xpath = "//th/text()"
        assert function.parse_xpath(htmldata, xpath) == ["编号", "姓名", "电话", "检测结果", "检测时间"]
        xpath = "//button/@onclick"
        assert function.parse_xpath(htmldata, xpath) == ["select()"]
        xpath = "//th"
        assert function.parse_xpath(htmldata, xpath) == [
            "<th>编号</th>",
            "<th>姓名</th>",
            "<th>电话</th>",
            "<th>检测结果</th>",
            "<th>检测时间</th>",
        ]
        xpath = "//error"
        assert function.parse_xpath(htmldata, xpath) == []

        try:
            xpath = "//error"
            ans = function.parse_xpath(jsondata, xpath)
            assert False
        except Exception as e:
            assert True

    def test_parse_regex(self, function: Function, htmldata, jsondata):
        """
        测试parse_regex函数
        """
        regex = "<th>(.*?)</th>"
        assert function.parse_regex(htmldata, regex) == ["编号", "姓名", "电话", "检测结果", "检测时间"]
        regex = 'onclick="(.*?)"'
        assert function.parse_regex(htmldata, regex) == ["select()"]
        regex = "<error>"
        assert function.parse_regex(htmldata, regex) == []

        regex = "'(.*?)'"
        assert function.parse_regex(jsondata, regex) == [
            "str",
            "string",
            "list",
            "dict",
            "key",
            "value",
            "list_dict",
            "key",
            "value1",
            "key",
            "value2",
        ]
        regex = "编号：(.*?),"
        assert function.parse_regex(jsondata, regex) == []

    def test_parse_css(self, function: Function, htmldata, jsondata):
        """
        测试parse_css函数
        """
        css = "th"
        assert function.parse_css(htmldata, css) == [
            "<th>编号</th>",
            "<th>姓名</th>",
            "<th>电话</th>",
            "<th>检测结果</th>",
            "<th>检测时间</th>",
        ]
        css = "error"
        assert function.parse_css(htmldata, css) == []

        try:
            css = "error"
            ans = function.parse_css(jsondata, css)
            assert False
        except Exception as e:
            assert True
