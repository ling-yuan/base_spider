from scrapy.cmdline import execute

if __name__ == "__main__":

    config = [
        {
            "request": {
                "type": "api",  # api/browser
                "url": "https://www.cnblogs.com/",
                "iteration_times": 1,  # 迭代次数
                "method": "get",  # get/post...
            },
            "response": {
                "type": "html",  # json/html/browser
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
                        "name": "next_url",
                        "value": '{xpath://a[@class="post-item-title"]/@href}',
                        "type": "url",
                    },
                ],  # 解析字段的列表
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
                    },
                ],
            },
        },
    ]

    # print(base64.b64encode(str(config).encode('utf-8')))

    execute(
        [
            "scrapy",
            "crawl",
            "base_spider",
            "-a",
            "config=" + str(config),
            "-o tmp.json",
        ]
    )
