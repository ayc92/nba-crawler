# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.contrib.exporter import JsonLinesItemExporter
from NBACrawler import settings
from NBACrawler.items import (
    PlayerInfoItem
)

class PlayerPipeline(object):
    def __init__(self, *args, **kwargs):
        self.player_info_file = None
        self.player_info_exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.player_info_file = open("%s/output/player_info.json" % settings.PROJECT_ROOT, 'wb')
        self.player_info_exporter = JsonLinesItemExporter(self.player_info_file)
        self.player_info_exporter.start_exporting()

    def spider_closed(self, spider):
        self.player_info_exporter.finish_exporting()
        self.player_info_file.close()

    def process_item(self, item, spider):
        if isinstance(item, PlayerInfoItem):
            self.player_info_exporter.export_item(item)
        return item
