# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
from urllib.parse import urlparse

from scrapy.pipelines.images import ImagesPipeline


class EtinexPipeline(object):
    def process_item(self, item, spider):
        return item

class MyImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        return 'original/' + os.path.basename(urlparse(request.url).path)