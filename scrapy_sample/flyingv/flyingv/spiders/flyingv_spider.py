# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from flyingv.items import FlyingvItem

class MySpider(CrawlSpider):
	name = 'flyingv'
	allowed_domains = ['flyingv.cc']
	start_urls = ['https://www.flyingv.cc/type/online']

	def parse(self, response):
		projects = response.xpath('//*[@id="isotope-portfolio-container"]/div')
		items = []	

		for project in projects:
			item = FlyingvItem()
			item['url'] = 'https://www.flyingv.cc'+project.xpath('div[2]/a/@href').extract()[0]
			item['name'] = project.xpath('div[2]/div/h5/text()').extract()
			item['owner'] = project.xpath('div[2]/div/div[2]/span/a/text()').extract()
			item['content'] = project.xpath('div[2]/a[1]/div[1]/div[2]/text()').extract()[0].encode('utf-8').replace("\r\n"," ").replace("\n"," ")
			item['money'] = project.xpath('div[2]/div/div[3]/text()').extract()
			item['pledge'] = project.xpath('div[2]/a[1]/div[1]/div/span[1]/text()').extract()
			item['percent'] = project.xpath('div[2]/a[1]/div[1]/div/span[2]/text()').extract()
			item['time'] = project.xpath('div[2]/div/div[4]/text()').extract()
			items.append(item)

		return items