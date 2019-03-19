# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class OldhouseItem(Item):
    # define the fields for your item here like:
    #标题
    title = Field()
    #户型
    type = Field()
    #面积大小
    area = Field()
    #总价
    totalprice = Field()
    #单价
    unitprice = Field()
    #小区名
    community = Field()
    #区域
    region = Field()







