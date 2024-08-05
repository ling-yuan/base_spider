# 测试配置

## 博客园

`解析参数` `解析后额外处理`

* [x] 成功运行

```python
[
    {
        "request": {
            "type": "api",
            "url": "https://www.cnblogs.com/",
            "iteration_times": 1,
            "method": "get",
        },
        "response": {
            "type": "html",
            "before": {},
            "fields": [
                {
                    "name": "title",
                    "value": '{xpath://a[@class="post-item-title"]/text()}',
                    "type": "str",
                },
                {
                    "name": "publish_time",
                    "value": '{xpath://*[@class="post-meta-item"]/span/text()}',
                    "type": "str",
                },
                {
                    "name": "url",
                    "value": '{xpath://a[@class="post-item-title"]/@href}',
                    "type": "url",
                },
                {
                    "name": "next_url",
                    "value": '{xpath://a[@class="post-item-title"]/@href}',
                    "type": "url",
                },
            ],
        },
    },
    {
        "request": {
            "type": "api",
            "url": "{var:next_url}",
            "method": "get",
        },
        "response": {
            "type": "html",
            "fields": [
                {
                    "name": "read_times",
                    "value": "{regex:阅读\((.*?)\)}",
                    "type": "int",
                    "after_process": [{"name": "str_extract_by_regex", "args": "\\d+"}],
                },
            ],
        },
    },
]
```

## 武招通

`参数使用`

* [x] 成功运行

```python
[
    {
        "request": {
            "type": "api",
            "url": "https://mobile.whzbtb.com/wzt-server/winningPublicity/list",
            "method": "post",
            "iteration_times": 1,
            "form_params": {"current": "{function:add(1)}"},
        },
        "response": {
            "type": "json",
            "fields": [
                {
                    "name": "title",
                    "value": "{jsonpath:$.data.records[*].prjName}",
                    "type": "str",
                },
                {
                    "name": "url",
                    "value": "https://mobile.whzbtb.com/wzt-server/winningPublicity/detail?id={jsonpath:$.data.records[*].id}",
                    "type": "str",
                },
                {
                    "name": "next_url",
                    "value": "https://mobile.whzbtb.com/wzt-server/winningPublicity/detail?id={jsonpath:$.data.records[*].id}",
                    "type": "str",
                },
                {
                    "name": "next_method",
                    "value": "post",
                    "type": "str",
                },
            ],
        },
    },
    {
        "request": {
            "type": "api",
            "url": "",
            "method": "post",
            "iteration_times": 1,
        },
        "response": {
            "type": "json",
            "fields": [
                {
                    "name": "agencyCorp",
                    "value": "{jsonpath:data.tbWinningPublicity.agencyCorp}",
                    "type": "str",
                },
            ],
        },
    },
]
```

## Agemys

`多页问题`

* [x] 成功运行

```python
[
    {
        "request": {
            "type": "api",
            "url": "https://www.agedm.org/detail/2022028{function:add(6,1)}",
            "method": "get",
            "iteration_times": 2,
        },
        "response": {
            "type": "html",
            "fields": [
                {
                    "name": "id",
                    "value": '{xpath://div[@class="tab-pane fade  show active "]/ul[@class="video_detail_episode"]/li/a/text()}',
                    "type": "str",
                },
                {
                    "name": "source_url",
                    "value": '{xpath://div[@class="tab-pane fade  show active "]/ul[@class="video_detail_episode"]/li/a/@href}',
                    "type": "str",
                },
            ],
            "save_fields": ["source_url"],
        },
    }
]
```

## Agemys

`多阶段` `重定向`

* [X] 成功运行

```python
[
    {
        "request": {
            "type": "api",
            "url": "https://www.agedm.org/",
            "method": "GET",
            "iteration_times": 1,
            "meta": {
                "proxy": "",
            },
        },
        "response": {
            "type": "html",
            "fields": [
                {
                    "name": "name",
                    "value": '{xpath://div[@class="video_item"]/div[2]/a/text()}',
                    "type": "str",
                },
                {
                    "name": "next_url",
                    "value": '{xpath://div[@class="video_item"]/div[2]/a/@href}',
                    "type": "str",
                },
            ],
        },
    },
    {
        "request": {
            "type": "api",
            "url": "{var:next_url}",
            "method": "get",
            "iteration_times": 2,
            "meta": {
                "proxy": "",
            },
        },
        "response": {
            "type": "html",
            "fields": [
                {
                    "name": "video_title",
                    "value": '{xpath://div[@class="tab-pane fade  show active "]/ul[@class="video_detail_episode"]/li/a/text()}',
                    "type": "str",
                },
                {
                    "name": "source_url",
                    "value": '{xpath://div[@class="tab-pane fade  show active "]/ul[@class="video_detail_episode"]/li/a/@href}',
                    "type": "str",
                },
            ],
            "save_fields": ["name", "video_title", "source_url"],
        },
    },
]
```
