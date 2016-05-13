# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ptt.items import PttItem
import re

class PttSpider(CrawlSpider):
	name = 'ptt'
	allowed_domains = ['ptt.cc']
	start_urls = ['https://www.ptt.cc/bbs/creditcard/index%s.html' % (i) for i in range(1700,1701)]
	
	# Extract links matching '/bbs/creditcard/M' and parse them with the spider's method parse_item
	rules = (
		Rule(LinkExtractor(allow=('/bbs/creditcard/M')), callback='parse_item', follow=True),
	)
	
	#def start_requests(self):
		#for url in self.start_urls:
			#yield scrapy.Request(url, cookies={'over18':'1'}, callback=self.parse)	

	def parse_item(self, response):		
		push_reg = re.compile('(\s*?)(</span>){0,1}(</div>){0,1}<div class="push"><span class="(.*)hl push-tag">(?P<PUSH>.+?) </span><span class="f3 hl push-userid">(?P<ID>.+?)</span><span class="f3 push-content">:(?P<CONTENT>.+?)</span><span class="push-ipdatetime">(\s*?)((?P<PUSHIP>\S+)( +)){0,1}(?P<DATE>\S+)( +)(?P<TIME>\S+?)$')
		title_reg = re.compile('(\s*?)<div id="main-content" class="bbs-screen bbs-content"><div class="article-metaline"><span class="article-meta-tag">作者</span><span class="article-meta-value">(?P<ID>.+?) \((.*)\)</span></div><div class="article-metaline-right"><span class="article-meta-tag">(\S+)</span><span class="article-meta-value">(?P<BOARD>.+?)</span></div><div class="article-metaline"><span class="article-meta-tag">標題</span><span class="article-meta-value">(?P<TITLE>.+?)</span></div><div class="article-metaline"><span class="article-meta-tag">時間</span><span class="article-meta-value">(\S+)( +)(?P<MONTH>\w+?)( +)(?P<DAY>\d+?)( +)(?P<TIME>\S+?)( +)(?P<YEAR>\d+?)</span></div>')
		author_push_reg = re.compile('</span></div>(?P<CONTENT>.+)')
		push_end_reg = re.compile('</span></div></div>')
		iframe_reg = re.compile('(.*)</iframe>(.*)') #for deleting youtube
		ip_reg = re.compile('</span>◆ From: (?P<IP>[0-9.]+)')
		ip_ch_reg = re.compile('<span class="f2">※ 發信站: 批踢踢實業坊\(ptt.cc\), 來自: (?P<IP>[0-9.]+)')

		STATUS = "TITLE"
		POST_CONTENT = ""
		
		# Post Information includes POST_AUTHOR POST_YEAR POST_MONTH POST_DATE POST_BOARD POST_TITLE POST_IP
		items = []
		for line in response.body.splitlines():
			if STATUS == "TITLE":
				T_MATCH = title_reg.match(line)
				
				if T_MATCH:
					PUSH_NO = 0
					ID = response.url
					MONTH_DICT = {'Jan':'1', 'Feb':'2', 'Mar':'3', 'Apr':'4', 'May':'5', 'Jun':'6', 'Jul':'7', 'Aug':'8', 'Sep':'9', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
					POST_AUTHOR = T_MATCH.group('ID')
					POST_BOARD = T_MATCH.group('BOARD')
					POST_TITLE = T_MATCH.group('TITLE')
					POST_YEAR = T_MATCH.group('YEAR')
					POST_MONTH = MONTH_DICT[T_MATCH.group('MONTH')]
					POST_DAY = T_MATCH.group('DAY')
					POST_TIME = T_MATCH.group('TIME')
					POST_DATE = POST_YEAR+'/'+POST_MONTH+'/'+POST_DAY
					
					STATUS = "CONTENT"
					continue
			
			if STATUS == "CONTENT":
				IP_MATCH = ip_reg.match(line)
				IP_CH_MATCH = ip_ch_reg.match(line)
			
				if IP_MATCH or IP_CH_MATCH:
					POST_IP = IP_MATCH.group("IP") if IP_MATCH else IP_CH_MATCH.group("IP")
					POST_CONTENT = str_clean(POST_CONTENT.replace('\n', ''))
	
					item = PttItem()
					assign_value(item, [ID, POST_BOARD, POST_AUTHOR, POST_TITLE, POST_AUTHOR,'POST',POST_CONTENT,POST_DATE,POST_TIME,POST_IP,str(PUSH_NO)])
					items.append(item)
		
					PUSH_NO = PUSH_NO + 1
					STATUS = "PUSH"
					
				elif re.search('<span class="f2">',line) or re.search('</span>',line):
					continue
					
				else:
					POST_CONTENT = POST_CONTENT + str_clean(line)
			
			if STATUS == "PUSH":
				P_MATCH = push_reg.match(line)
				AU_P_MATCH = author_push_reg.match(line)
				PUSH_END_MATCH = push_end_reg.match(line)
				IFRAME_MATCH = iframe_reg.match(line)
				
				if PUSH_END_MATCH:
					break
					
				elif P_MATCH:			
					if P_MATCH.group('DATE')>='01/01' and P_MATCH.group('DATE')<='01/31' and POST_MONTH=='12':
						PUSH_YEAR = str(int(POST_YEAR) + 1)
					else:
						PUSH_YEAR = POST_YEAR
					
					item = PttItem()
					assign_value(item, [ID,POST_BOARD, POST_AUTHOR, POST_TITLE, P_MATCH.group('ID').strip() ,P_MATCH.group('PUSH'),str_clean(P_MATCH.group('CONTENT')),PUSH_YEAR+'/'+P_MATCH.group('DATE'),P_MATCH.group('TIME'),"",str(PUSH_NO)])
					items.append(item)
					
					PUSH_NO = PUSH_NO + 1
					
				elif AU_P_MATCH and not (IFRAME_MATCH):
					item = PttItem()
					assign_value(item, [ID,POST_BOARD, POST_AUTHOR, POST_TITLE, POST_AUTHOR,'REPLY',str_clean(AU_P_MATCH.group('CONTENT')),POST_DATE,"","",str(PUSH_NO)])
					items.append(item)
					
					PUSH_NO = PUSH_NO + 1		
		
		return items
		
def str_clean(str):
	"To clean string by removing the comma, and hyperlink tags"
	url_reg = re.compile('(.*?)<a href="(.+?)" target="_blank" rel="nofollow">(?P<URL>.+?)</a>')
	url_match = url_reg.match(str)

	if url_match:
		URL = url_match.group('URL')
		return re.sub('<a href="(.+?)" target="_blank" rel="nofollow">(?P<URL>.+?)</a>',URL,str).replace(',','')
	else:
		return str.replace(',','')
		
def assign_value(item, ROW):
	"To assign value to item"
	ROW = [x.strip() for x in ROW]
	item["URL"] = ROW[0]
	item["BOARD"] = ROW[1]
	item["POST_ID"] = ROW[2]
	item["POST_TITLE"] = ROW[3]
	item["PUSH_ID"] = ROW[4]
	item["PUSH_TYPE"] = ROW[5]
	item["CONTENT"] = ROW[6]
	item["DATE"] = ROW[7]
	item["TIME"] = ROW[8]
	item["POST_IP"] = ROW[9]
	item["PUSH_NO"] = ROW[10]