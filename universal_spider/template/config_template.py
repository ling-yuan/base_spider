default_stage_template = {
    "request": {  # 当前阶段请求
        "type": "",  # api/browser
        "url": "",
        "method": "",  # get/post...
        "iteration_times": 1,  # 当前阶段多个页面，迭代次数
        "meta": {
            "proxy": "",  # 当前阶段请求的代理
            "dont_redirect": False,  # 当前阶段请求是否重定向
            "redirect_ttl": 5,  # 当前阶段请求最大重定向次数
        },  # 当前阶段请求的meta信息，用于传递给下一阶段
        "headers": {},
        "query_params": {},
        "json_params": {},
        "form_params": {},
        "dont_filter": True,
        "extra_params": {},
    },
    "response": {  # 当前阶段响应
        "type": "",  # json/html/browser
        "before_parse": [],
        "fields": [],  # 解析字段的列表 [default_field_template]
        "save_fields": [],  # 保存字段的列表 上边所有解析后的字段最终需要保存的字段名称 (仅最后阶段使用该值)
        "extra_params": {},
    },
}

default_field_template = {
    "name": "",  # 字段名称
    "value": "",  # 字段值，其中可变值使用{}包裹  # {jsonpath:path} {xpath://table} {css:ul>li} {regex:[0-9]+} {var:var_name} {function:function_name(args)}
    "type": "",  # 字段类型  # str、json、date、file等
    "default": "",  # 默认值  # 默认为空
    "befor_process": [  # 字段解析前，顺序执行的前处理方法 # 可选，默认为空
        {"name": "", "args": ""},  # 处理方法名称  # 处理方法参数，其中可变值使用{}包裹
    ],
    "after_process": [  # 字段解析后，顺序执行的后处理方法 # 可选，默认为空
        {"name": "", "args": ""},  # 处理方法名称  # 处理方法参数，其中可变值使用{}包裹
    ],
    "save_length": 0,  # 字段长度，默认为0，表示不限制 (1表示所有匹配生成的列表合并，其余值均不合法)
    "save_method": "",  # 字段解析后，保存方法  # replace、append、add 默认替换原本的同名字段
}
