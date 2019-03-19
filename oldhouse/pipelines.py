# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook

class OldhouseExcelPipeline(object):
    def __init__(self):
        pass
    def open_spider(self, spider):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = "苏州二手房"
        self.ws.column_dimensions["A"].width = 30
        self.ws.column_dimensions["B"].width = 10
        self.ws.column_dimensions["F"].width = 15
        self.ws.row_dimensions[1].height = 20
        self.ws.append(['标题', '户型', '面积', '总价（万）', '单价（元/m^2)', '小区名', '区域'])  # 设置表头

    def process_item(self, item, spider):
        line = [item['title'], item['type'], item['area'], item['totalprice'], item['unitprice'], item['community'],
                item['region']]
        self.ws.append(line)
        return item
    def close_spider(self, spider):
        self.wb.save('house.xlsx')

