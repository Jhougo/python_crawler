# -*- coding: utf-8 -*-

from scrapy.item import Item, Field

class PttItem(Item):
	URL = Field()
	BOARD = Field()
	POST_ID = Field()
	POST_TITLE = Field()
	PUSH_ID = Field()
	PUSH_TYPE = Field()
	CONTENT = Field()
	DATE = Field()
	TIME = Field()
	POST_IP = Field()
	PUSH_NO = Field()
