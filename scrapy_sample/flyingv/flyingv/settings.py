# -*- coding: utf-8 -*-

SPIDER_MODULES = ['flyingv.spiders']
NEWSPIDER_MODULE = 'flyingv.spiders'
DEFAULT_ITEM_CLASS = 'flyingv.items.Website'

ITEM_PIPELINES = {'flyingv.pipelines.WriteToCsv': 1}

# Output Settings (filename & fields order)
csv_file_path = "flyingv.csv"
csv_export_fields = [
    'url', 
    'name',
    'owner',
    'content',
    'money',
    'pledge',
	'percent',
	'time',
]

DOWNLOAD_HANDLERS = {'s3': None}

DOWNLOAD_DELAY = 3
DEPTH_LIMIT = 1