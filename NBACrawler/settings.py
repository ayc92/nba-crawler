# -*- coding: utf-8 -*-

# Scrapy settings for NBACrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

BOT_NAME = 'NBACrawler'

SPIDER_MODULES = ['NBACrawler.spiders']
NEWSPIDER_MODULE = 'NBACrawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'NBACrawler (+http://www.yourdomain.com)'

CONCURRENT_REQUESTS_PER_DOMAIN = 12

ITEM_PIPELINES = {
    'NBACrawler.pipelines.PlayerPipeline': 0
}
