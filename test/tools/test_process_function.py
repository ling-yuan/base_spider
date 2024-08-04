import sys_path
import pytest
from universal_spider.tools.process_function import ProcessFunction


class TestProcessFunction:

    @pytest.fixture
    def process_function(self):
        return ProcessFunction()

    @pytest.fixture
    def stringdata_str(self):
        return "时间:2024/08/04 文章标题1"

    @pytest.fixture
    def stringdata_list(self):
        return [
            "时间:2024/08/04 文章标题1",
            "时间:2024/08/04 文章标题2",
            "时间:2024/08/04 文章标题3",
        ]

    @pytest.fixture
    def htmldata_str(self):
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

    @pytest.fixture
    def htmldata_list(self):
        return [
            """
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
            """,
            """
            <form>
                <input type="text" name="username" placeholder="用户名">
                <input type="password" name="password" placeholder="密码">
                <button type="submit">登录</button>
            </form>
            """,
        ]

    @pytest.fixture
    def htmldata_with_style_str(self):
        return '<a style="color: red;">这是一个链接</a>'

    @pytest.fixture
    def htmldata_with_style_list(self):
        return [
            '<a style="color: red;">这是一个链接</a>',
            "<a>这是另一个链接</a>",
        ]

    def test_str_remove_by_regex(self, process_function: ProcessFunction, stringdata_str, stringdata_list):
        data = stringdata_str
        func_params = "时间"
        result = process_function.str_remove_by_regex(data, func_params)
        assert result == ":2024/08/04 文章标题1"

        data = stringdata_list
        func_params = "\d+"
        result = process_function.str_remove_by_regex(data, func_params)
        assert result == [
            "时间:// 文章标题",
            "时间:// 文章标题",
            "时间:// 文章标题",
        ]

        # data = {}
        # func_params = "时间"
        # result = process_function.str_remove_by_regex(data, func_params)
        # assert result == {}

    def test_str_replace_by_regex(self, process_function: ProcessFunction, stringdata_str, stringdata_list):
        data = stringdata_str
        func_params = "时间,金钱"
        result = process_function.str_replace_by_regex(data, func_params)
        assert result == "金钱:2024/08/04 文章标题1"

        data = stringdata_list
        func_params = "\d+,666"
        result = process_function.str_replace_by_regex(data, func_params)
        assert result == [
            "时间:666/666/666 文章标题666",
            "时间:666/666/666 文章标题666",
            "时间:666/666/666 文章标题666",
        ]

        # data = {}
        # func_params = "时间,金钱"
        # result = process_function.str_replace_by_regex(data, func_params)
        # assert result == {}

    def test_html_removetag_by_xpath(self, process_function: ProcessFunction, htmldata_str, htmldata_list):
        data = htmldata_str
        func_params = "//th"
        result = process_function.html_removetag_by_xpath(data, func_params)
        assert (
            result
            == """<html><body>
            <table>
                <tr>
                    </tr>
            </table>
            <button onclick="select()">查询</button>
            <script type="text/javascript" src="js/yezhu.js"/>
        </body>
        </html>"""
        )

        data = htmldata_list
        func_params = "//th"
        result = process_function.html_removetag_by_xpath(data, func_params)
        assert result == [
            """<html><body>
                <table>
                    <tr>
                        </tr>
                </table>
                <button onclick="select()">查询</button>
                <script type="text/javascript" src="js/yezhu.js"/>
            </body>
            </html>""",
            """<html><body><form>
                <input type="text" name="username" placeholder="用户名"/>
                <input type="password" name="password" placeholder="密码"/>
                <button type="submit">登录</button>
            </form>
            </body></html>""",
        ]

    def test_html_removestyle_by_xpath(
        self, process_function: ProcessFunction, htmldata_with_style_str, htmldata_with_style_list
    ):
        data = htmldata_with_style_str
        func_params = "//*"
        result = process_function.html_removestyle_by_xpath(data, func_params)
        assert result == "<html><body><a>这是一个链接</a></body></html>"

        data = htmldata_with_style_list
        func_params = "//*"
        result = process_function.html_removestyle_by_xpath(data, func_params)
        assert result == [
            "<html><body><a>这是一个链接</a></body></html>",
            "<html><body><a>这是另一个链接</a></body></html>",
        ]

    def test_html_replacetag_by_xpath(
        self, process_function: ProcessFunction, htmldata_with_style_str, htmldata_with_style_list
    ):
        data = htmldata_with_style_str
        func_params = "//a,p"
        result = process_function.html_replacetag_by_xpath(data, func_params)
        assert result == '<html><body><p style="color: red;">这是一个链接</p></body></html>'

        data = htmldata_with_style_list
        func_params = "//a,p"
        result = process_function.html_replacetag_by_xpath(data, func_params)
        assert result == [
            '<html><body><p style="color: red;">这是一个链接</p></body></html>',
            "<html><body><p>这是另一个链接</p></body></html>",
        ]
