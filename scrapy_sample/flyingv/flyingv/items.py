# -*- coding: utf-8 -*-

from scrapy.item import Item, Field

class FlyingvItem(Item):
	url = Field()
	name = Field()
	owner = Field()
	content = Field()
	money = Field()
	pledge = Field()
	percent = Field()
	time = Field()

