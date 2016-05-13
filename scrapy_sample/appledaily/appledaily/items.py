# -*- coding: utf-8 -*-

from scrapy.item import Item, Field

class AppledailyItem(Item):
	title = Field()
	content = Field()
	date = Field()
	url = Field()
