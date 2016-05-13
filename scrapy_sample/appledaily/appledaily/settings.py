# -*- coding: utf-8 -*-

SPIDER_MODULES = ['appledaily.spiders']
NEWSPIDER_MODULE = 'appledaily.spiders'
DEFAULT_ITEM_CLASS = 'appledaily.items.Website'

ITEM_PIPELINES = {'appledaily.pipelines.SubstituteWordsPipeline':1,
				  'appledaily.pipelines.WriteToCsv': 2,}
				  
# Output Settings (filename & fields order)
csv_file_path = "appledaily.csv"
csv_export_fields = [
    'date', 
    'title',
    'content',
    'url',
]

DOWNLOAD_HANDLERS = {'s3': None}

DOWNLOAD_DELAY = 3
DEPTH_LIMIT = 2