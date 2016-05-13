# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from flyingv import settings

class WriteToCsv(object):
	@classmethod

	def process_item(self, item, spider):
		self.file = open(settings.csv_file_path, 'ab+')
		self.exporter = CsvItemExporter(self.file, include_headers_line=False)
		self.exporter.fields_to_export = settings.csv_export_fields
		self.exporter.export_item(item)
		return item