# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from appledaily import settings

class WriteToCsv(object):
	@classmethod
	
	def process_item(self, item, spider):
		self.file = open(settings.csv_file_path, 'ab+')
		self.exporter = CsvItemExporter(self.file, include_headers_line=False)
		self.exporter.fields_to_export = settings.csv_export_fields
		self.exporter.export_item(item)
		return item

class SubstituteWordsPipeline(object):
	"""A pipeline for substitute items which contain certain words in their title or content"""
	
	def process_item(self, item, spider):
		item['title'] = item['title'][0].encode('utf-8').replace(' | 蘋果日報','')
		
		item['content'] = item['content'].replace('【蘋論陣線】：最新評論及獨立媒體每日總覽','')
		item['content'] = item['content'].replace('有話要說 投稿「即時論壇」','')
		item['content'] = item['content'].replace('onlineopinions@appledaily.com.tw','')    

		return item