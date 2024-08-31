from scrapy.cmdline import execute

if __name__ == "__main__":

    config = [
        {
            "request": {
                "type": "api",
                "url": "https://www.agedm.org/detail/20100003",
                "method": "GET",
                "iteration_times": "1",
                "dont_filter": "True",
            },
            "response": {
                "type": "html",
                "save_fields": [],
                "fields": [
                    {
                        "name": "name",
                        "type": "str",
                        "save_length": "0",
                        "value": '缘之空 - {xpath://div[@id="playlist-source-panda"]//li/a/text()}',
                        "default": "",
                        "save_method": "replace",
                        "after_process": [],
                    },
                    {
                        "name": "next_url",
                        "type": "str",
                        "save_length": "0",
                        "value": '{xpath://div[@id="playlist-source-panda"]//li/a/@href}',
                        "default": "",
                        "save_method": "replace",
                        "after_process": [],
                    },
                ],
            },
        },
        {
            "request": {
                "type": "api",
                "method": "GET",
                "iteration_times": "1",
                "dont_filter": "True",
                "headers": {"host": "www.agedm.org"},
            },
            "response": {
                "type": "html",
                "save_fields": ["name", "page_url"],
                "fields": [
                    {
                        "name": "page_url",
                        "type": "str",
                        "save_length": "0",
                        "value": '{xpath://iframe[@id="iframeForVideo"]/@src}',
                        "default": "",
                        "save_method": "replace",
                        "after_process": [],
                    }
                ],
            },
        },
    ]

    execute(
        [
            "scrapy",
            "crawl",
            "base_spider",
            "-a",
            "config=" + str(config),
        ]
    )
