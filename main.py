from scrapy.cmdline import execute

if __name__ == "__main__":

    config = []

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
