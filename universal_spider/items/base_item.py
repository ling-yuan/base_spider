import scrapy


class BaseItem(scrapy.Item):

    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = scrapy.Field()
        return super().__setitem__(key, value)
