import time
import pytest

from universal_spider.tools.replacer import Replacer


class TestReplacer:

    @pytest.fixture
    def replacer(self):
        return Replacer()

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
                <tr class="row">
                    <th class="head">编号</th>
                    <th class="head">姓名</th>
                    <th class="head">电话</th>
                    <th class="head">检测结果</th>
                </tr>
            </table>
            <button onclick="select()">查询</button>
            <script type="text/javascript" src="js/yezhu.js"></script>
        </body>
        """

    @pytest.fixture
    def item(self):
        return {
            "name": ["张三", "李四", "王五"],
            "age": [18, 19, 20],
            "class": "一班",
        }

    def test_replace_function(self, replacer: Replacer, htmldata, jsondata, item):
        # add方法
        value = "当前页数：{function:add(1,2)}"
        new_value, ans = replacer.replace(value, htmldata, item=item)
        assert new_value == "当前页数：{function:add(3,2)}"
        assert ans == ["当前页数：1"]

        value = "当前页数：{function:add(5)}"
        new_value, ans = replacer.replace(value, jsondata, item=item)
        assert new_value == "当前页数：{function:add(6)}"
        assert ans == ["当前页数：5"]

        # now_timestamp方法
        value = "现在时间：{function:now_timestamp()}"
        assert replacer.replace(value, htmldata, item=item) == (value, ["现在时间：" + str(int(time.time()))])

    def test_replace_xpath(self, replacer: Replacer, htmldata, jsondata, item):
        # 内容
        value = "姓名：{xpath://th/text()}"
        new_value, ans = replacer.replace(value, htmldata, item=item)
        assert new_value == value
        assert ans == ["姓名：编号", "姓名：姓名", "姓名：电话", "姓名：检测结果"]

        # 属性
        value = "姓名：{xpath://button/@onclick} qwer"
        new_value, ans = replacer.replace(value, htmldata, item=item)
        assert new_value == value
        assert ans == ["姓名：select() qwer"]

    def test_replace_jsonpath(self, replacer: Replacer, htmldata, jsondata, item):
        # string
        value = "姓名：{jsonpath:$.str}"
        new_value, ans = replacer.replace(value, jsondata, item=item)
        assert new_value == value
        assert ans == ["姓名：string"]
        # list
        value = "姓名：{jsonpath:$.list[0]}"
        new_value, ans = replacer.replace(value, jsondata, item=item)
        assert new_value == value
        assert ans == ["姓名：1"]
        value = "姓名：{jsonpath:$.list}"
        new_value, ans = replacer.replace(value, jsondata, item=item)
        assert new_value == value
        assert ans == ["姓名：1", "姓名：2", "姓名：3"]
        # list_dict
        value = "姓名：{jsonpath:$.list_dict[0].key}"
        new_value, ans = replacer.replace(value, jsondata, item=item)
        assert new_value == value
        assert ans == ["姓名：value1"]
        value = "姓名：{jsonpath:$.list_dict[:].key}"
        new_value, ans = replacer.replace(value, jsondata, item=item)
        assert new_value == value
        assert ans == ["姓名：value1", "姓名：value2"]

    def test_replace_css(self, replacer: Replacer, htmldata, jsondata, item):
        value = "姓名：{css:tr>th}"
        new_value, ans = replacer.replace(value, htmldata, item=item)
        assert new_value == value
        assert ans == [
            '姓名：<th class="head">编号</th>',
            '姓名：<th class="head">姓名</th>',
            '姓名：<th class="head">电话</th>',
            '姓名：<th class="head">检测结果</th>',
        ]

        value = "{css:button}"
        new_value, ans = replacer.replace(value, htmldata, item=item)
        assert new_value == value
        assert ans == ['<button onclick="select()">查询</button>']

    def test_replace_regex(self, replacer: Replacer, htmldata, jsondata, item):
        value = '{regex:<th class="head">(.*?)</th>}'
        new_value, ans = replacer.replace(value, htmldata, item=item)
        assert new_value == value
        assert ans == ["编号", "姓名", "电话", "检测结果"]

        value = "{regex:'(.*?)'}"
        new_value, ans = replacer.replace(value, jsondata, item=item)
        assert new_value == value
        assert ans == ["str", "string", "list", "dict", "key", "value", "list_dict", "key", "value1", "key", "value2"]

    def test_replace_var(self, replacer: Replacer, htmldata, jsondata, item):
        value = "{var:name}"
        new_value, ans = replacer.replace(value, htmldata, item=item)
        assert new_value == value
        assert ans == ["张三", "李四", "王五"]

        value = "{var:age}"
        new_value, ans = replacer.replace(value, htmldata, item=item)
        assert new_value == value
        assert ans == ["18", "19", "20"]

        value = "{var:class}"
        new_value, ans = replacer.replace(value, jsondata, item=item)
        assert new_value == value
        assert ans == ["一班"]

    def test_replace_muti_params(self, replacer: Replacer, htmldata, jsondata, item):
        value = "页数：{function:add(5)} title： {jsonpath:$.list}"
        new_value, ans = replacer.replace(value, jsondata, item=item)
        assert new_value == "页数：{function:add(6)} title： {jsonpath:$.list}"
        assert ans == [
            "页数：5 title： 1",
            "页数：5 title： 2",
            "页数：5 title： 3",
        ]

        value = {"页码": "{function:add(5)}", "标题": "{jsonpath:$.list}"}
        new_value, ans = replacer.replace(value, jsondata, item=item)
        assert new_value == {"页码": "{function:add(6)}", "标题": "{jsonpath:$.list}"}
        assert ans == [
            {"页码": "5", "标题": "1"},
            {"页码": "5", "标题": "2"},
            {"页码": "5", "标题": "3"},
        ]
