import ast
import re
from universal_spider.tools.function import Function

# 可变参数pattern
VARIABLE_CONTENT_PATTERN = r'\{(?P<type>[a-zA-Z_]+)\:(?P<content>.*?)\}'
# 可变参数中 函数pattern
FUNCTION_NAME_PATTERN = r'(?P<func_name>[a-zA-Z_]+)'
FUNCTION_PARAMS_PATTERN = r'\((?P<params>.*?)\)'


class Replacer(Function):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def replace(self, value: str | list | dict, content="", *args, **kwargs):
        '''
        根据content的内容，替换value中的可变值
        
        :param value: 可变值
        :param content: 替换依据
        :param args: 其他参数
        :param kwargs: 其他参数 其中item在使用变量替换时有用
        :return: 返回 原值和替换后的值组成的列表 ("姓名：{jsonpath:$.[*].name}",["姓名：张三", "姓名：李四"])
        '''
        # 获取可变参数
        variable_content = re.finditer(VARIABLE_CONTENT_PATTERN, str(value))
        # 可变值下次匹配值 字典
        next_value_dict = {}
        # 可变值匹配结果 字典
        match_dict = {}
        for item in variable_content:
            func_type = item.group('type')
            func_content = item.group('content')
            matched_str = "{" + func_type + ":" + func_content + "}"
            ans = None
            if func_type == 'function':
                next_func_content, ans = self._replace_function(func_content, content, *args, **kwargs)
                next_value_dict[matched_str] = "{" + func_type + ":" + next_func_content + "}"
            elif func_type == 'xpath':
                ans = self._replace_xpath(func_content, content, *args, **kwargs)
            elif func_type == 'css':
                ans = self._replace_css(func_content, content, *args, **kwargs)
            elif func_type == 'regex':
                ans = self._replace_regex(func_content, content, *args, **kwargs)
            elif func_type == 'jsonpath':
                ans = self._replace_jsonpath(func_content, content, *args, **kwargs)
            elif func_type == 'var':
                ans = self._replace_var(func_content, content, *args, **kwargs)
            match_dict['{' + func_type + ':' + func_content + '}'] = ans
        # 替换内容
        value, replaced_value = self.replace_content(value, match_dict, next_value_dict, *args, **kwargs)
        # 返回：原值 和 替换后值的列表
        return value, replaced_value

    def replace_content(self, value: str | list | dict, match_dict: dict, next_value_dict: dict, *args, **kwargs):
        """
        根据match_dict中需要替换的内容，按照值长度最大的个数替换出最大个数的结果
        """
        if not match_dict:
            return value

        # value 的类型
        value_type = type(value)
        # value 转为字符串
        value = str(value)
        # 获取替换字典中值最长的
        l = max([len(i) for i in match_dict.values()])
        # 设置长度一致
        for k, v in match_dict.items():
            if len(v) != l:
                raise Exception("The length of the value matched to the variable parameter is inconsistent")
            elif len(v) == 1:
                match_dict[k] = v * l

        # 根据替换字典，生成替换结果
        ans = []
        for index in range(l):
            tmp_value = value
            for key in match_dict.keys():
                tmp_value = tmp_value.replace(key, str(match_dict[key][index]))
            ans.append(ast.literal_eval(tmp_value) if value_type in [dict, list] else tmp_value)

        # 生成下一次的替换的value
        for k, v in next_value_dict.items():
            value = value.replace(k, v)
        value = ast.literal_eval(value) if value_type in [dict, list] else value

        return value, ans

    def _replace_function(self, func_content, content, *args, **kwargs):
        func_name = re.findall(FUNCTION_NAME_PATTERN, func_content, re.S)[0]
        func_params = re.findall(FUNCTION_PARAMS_PATTERN, func_content, re.S)[0]

        func_name = func_name.strip()
        if func_name not in self.function_dict.keys():
            raise Exception('function not found')
        func = self.function_dict[func_name]
        next_params, ans = func(func_params, data=content)
        next_func_content = func_name + "(" + next_params + ")"
        return next_func_content, ans

    def _replace_xpath(self, func_content, content, *args, **kwargs):
        ans = self.parse_xpath(content, func_content, *args, **kwargs)
        return ans

    def _replace_css(self, func_content, content, *args, **kwargs):
        ans = self.parse_css(content, func_content, *args, **kwargs)
        return ans

    def _replace_regex(self, func_content, content, *args, **kwargs):
        ans = self.parse_regex(content, func_content, *args, **kwargs)
        return ans

    def _replace_jsonpath(self, func_content, content, *args, **kwargs):
        ans = self.parse_jsonpath(content, func_content, *args, **kwargs)
        return ans

    def _replace_var(self, func_content, content, *args, **kwargs):
        item = kwargs['item']
        ans = item[func_content]
        if isinstance(ans, list):
            return [str(i) for i in ans]
        else:
            return [str(ans)]
