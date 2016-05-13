# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from appledaily.items import AppledailyItem
import re

class MySpider(CrawlSpider):
	name = 'appledaily'
	allowed_domains = ['appledaily.com.tw']
	start_urls = ['http://www.appledaily.com.tw/appledaily/archive/20151108']

	# Extract links matching '/appledaily/article/headline/' and parse them with the spider's method parse_item
	rules = (
		Rule(LinkExtractor(allow=('/appledaily/article/headline/')), callback='parse_item', follow=True),
	)

	def parse_item(self, response):
		item = AppledailyItem()
		item['title'] = response.xpath('/html/head/title/text()').extract()
		item['url'] = response.url
		item['content'] = removeTag(response.xpath('//*[@id="maincontent"]/div[2]/article/div[2]').extract())
		item['date'] = response.xpath('//*[@id="maincontent"]/div[2]/article/div[1]/time/text()').extract()
		return item

def removeTag(content):
	removeScrip = re.subn(r'<(script).*?</\1>', '', " ".join([i.encode('utf-8') for i in content]), re.DOTALL)[0]
	removeTag = re.sub(r'<.*?>', '', removeScrip)
	return " ".join([i.strip() for i in removeTag.splitlines()])
	