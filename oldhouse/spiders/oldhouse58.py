
# -*- coding: utf-8 -*-


from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import *
import re
import base64
from io import BytesIO
from fontTools.ttLib import TTFont

class Oldhouse58Spider(CrawlSpider):
    name = 'oldhouse58'
    allowed_domains = ['su.58.com']
    start_urls = ['http://su.58.com/ershoufang/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class=list-info]//h2//a'), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_xpaths='//div[@class=pager]//a[@class=next]'), follow=True),
    )

    def parse_item(self, response):
        bs64_str = re.findall("charset=utf-8;base64,(.*?)'\)", response.text)[0]
        font = TTFont(BytesIO(base64.decodebytes(bs64_str.encode())))
        c = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap
        oldhouse = OldhouseItem()
        oldhouse['title'] = response.css('.c_333.f20::text').extract_first().strip()
        oldhouse['type'] = response.css('.house-basic-item2 .room .main::text').extract_first().strip()
        oldhouse['area'] = response.css('.house-basic-item2 .area .main::text').extract_first().strip()
        totalprice = response.css('.house-basic-item1 .price.strongbox::text').extract_first().strip()
        total_list = []
        for char in list(totalprice):
            decode_num = ord(char)
            if decode_num in c:
                num = c[decode_num]
                num = int(num[-2:]) - 1
                total_list.append(num)
            else:
                total_list.append(char)
        total_str_show = ''
        for num in total_list:
            total_str_show += str(num)
        oldhouse['totalprice'] =total_str_show
        unitprice = response.css('.house-basic-item1 .unit.strongbox::text').extract_first().replace(u'\xa0',u' ').split()[0]
        unit_list = []
        for char in list(unitprice):
            decode_num = ord(char)
            if decode_num in c:
                num = c[decode_num]
                num = int(num[-2:]) - 1
                unit_list.append(num)
            else:
                unit_list.append(char)
        unit_str_show = ''
        for num in unit_list:
            unit_str_show += str(num)
        oldhouse['unitprice'] = unit_str_show
        oldhouse['community'] = response.css('.house-basic-item3 li .c_000.mr_10 a:nth-child(1)::text').extract_first().strip()
        oldhouse['region'] = response.css('.house-basic-item3 li:nth-child(2) .c_000.mr_10 a:nth-child(1)::text').extract_first().strip()

