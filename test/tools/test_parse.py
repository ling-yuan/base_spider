import sys_path
import pytest
from universal_spider.tools.parse import JsonParser
from universal_spider.tools.parse import RegexParser
from universal_spider.tools.parse import XPathParser
from universal_spider.tools.parse import CssParser


class TestJsonParse:

    @pytest.fixture
    def json_parser(self):
        json_parser = JsonParser()
        return json_parser

    @pytest.fixture
    def json_data(self):
        return {
            "str": "张三",
            "dict": {
                "city": "北京",
                "country": "中国",
            },
            "list": ["篮球", "足球", "乒乓球"],
            "list_list": [
                [1, 2, 3],
                [4, 5, 6],
            ],
            "list_dict": [
                {"name": "张三", "age": 18},
                {"name": "李四", "age": 20},
            ],
        }

    def test_json_parse_str(self, json_parser, json_data):
        jsonpath = "$.str"
        result = json_parser.parse(json_data, jsonpath)
        assert result == ["张三"]

    def test_json_parse_list(self, json_parser, json_data):
        jsonpath = "$.list"
        result = json_parser.parse(json_data, jsonpath)
        assert result == ["篮球", "足球", "乒乓球"]

    def test_json_parse_dict(self, json_parser, json_data):
        jsonpath = "$.dict"
        result = json_parser.parse(json_data, jsonpath)
        assert result == [{"city": "北京", "country": "中国"}]

    def test_json_parse_list_dict(self, json_parser, json_data):
        jsonpath = "$.list_dict[*].name"
        result = json_parser.parse(json_data, jsonpath)
        assert result == ["张三", "李四"]

    def test_json_parse_list_list(self, json_parser, json_data):
        jsonpath = "$.list_list[*][1]"
        result = json_parser.parse(json_data, jsonpath)
        assert result == [2, 5]

    def test_json_parse_error(self, json_parser, json_data):
        jsonpath = "$.error"
        result = json_parser.parse(json_data, jsonpath)
        assert result == []


class TestRegexParse:

    @pytest.fixture
    def regex_parser(self):
        regex_parser = RegexParser()
        return regex_parser

    @pytest.fixture
    def html_content(self):
        return """
        <body>
            <table>
                <thead>
                    <tr>
                        <th>编号</th>
                        <th>姓名</th>
                        <th>电话</th>
                        <th>检测结果</th>
                        <th>检测时间</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
            <button onclick="select()">查询</button>
            <script type="text/javascript" src="js/yezhu.js"></script>
        </body>
        """

    @pytest.fixture
    def json_content(self):
        return {"list_list": [[1, "张三"], [2, "李四"]]}

    def test_regex_parse_html(self, regex_parser, html_content):
        regex = "<th>(.*?)</th>"
        result = regex_parser.parse(html_content, regex)
        assert result == ["编号", "姓名", "电话", "检测结果", "检测时间"]

    def test_regex_parse_json(self, regex_parser, json_content):
        regex = "\[(.*?)\]"
        result = regex_parser.parse(json_content, regex)
        assert result == [
            "[1, '张三'",
            "2, '李四'",
        ]

    def test_regex_parse_error(self, regex_parser, html_content, json_content):
        regex = r"<error>(.*?)</error>"
        result = regex_parser.parse(html_content, regex)
        assert result == []
        result = regex_parser.parse(json_content, regex)
        assert result == []


class TestXPathParser:

    @pytest.fixture
    def xpath_parser(self):
        xpath_parser = XPathParser()
        return xpath_parser

    @pytest.fixture
    def html_content(self):
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

    def test_xpath_parse(self, xpath_parser, html_content):
        result = xpath_parser.parse(html_content, "//button/@onclick")
        assert result == ["select()"]
        result = xpath_parser.parse(html_content, "//th/text()")
        assert result == ["编号", "姓名", "电话", "检测结果", "检测时间"]
        result = xpath_parser.parse(html_content, "//th")
        assert result == ["<th>编号</th>", "<th>姓名</th>", "<th>电话</th>", "<th>检测结果</th>", "<th>检测时间</th>"]

    def test_xpath_parse_error(self, xpath_parser, html_content):
        result = xpath_parser.parse(html_content, "//td")
        assert result == []


class TestCssParser:

    @pytest.fixture
    def css_parser(self):
        css_parser = CssParser()
        return css_parser

    @pytest.fixture
    def html_content(self):
        return """
        <body>
            <table>
                <tr>
                    <th>编号</th>
                    <th>姓名</th>
                    <th class="number">电话</th>
                    <th>检测结果</th>
                    <th>检测时间</th>
                </tr>
            </table>
            <button onclick="select()">查询</button>
            <script type="text/javascript" src="js/yezhu.js"></script>
        </body>
        """

    def test_css_parse(self, css_parser, html_content):
        result = css_parser.parse(html_content, "th")
        assert result == [
            "<th>编号</th>",
            "<th>姓名</th>",
            '<th class="number">电话</th>',
            "<th>检测结果</th>",
            "<th>检测时间</th>",
        ]
        result = css_parser.parse(html_content, "th.number")
        assert result == ['<th class="number">电话</th>']

    def test_css_parse_error(self, css_parser, html_content):
        result = css_parser.parse(html_content, "td")
        assert result == []
