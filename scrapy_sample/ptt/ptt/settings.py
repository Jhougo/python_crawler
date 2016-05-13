# -*- coding: utf-8 -*-

SPIDER_MODULES = ['ptt.spiders']
NEWSPIDER_MODULE = 'ptt.spiders'
DEFAULT_ITEM_CLASS = 'ptt.items.PttItem'

ITEM_PIPELINES = {'ptt.pipelines.WriteToCsv': 1}

# Output Settings (filename & fields order)
csv_file_path = "ptt_output.csv"
csv_export_fields = [
	'URL',
	'BOARD',
	'POST_ID',
	'POST_TITLE',
	'PUSH_ID',
	'PUSH_TYPE',
	'CONTENT',
	'DATE',
	'TIME',
	'POST_IP',
	'PUSH_NO',
]

DOWNLOAD_HANDLERS = {'s3': None}

DEPTH_LIMIT = 1
DOWNLOAD_DELAY = 3
RETRY_TIMES = 10