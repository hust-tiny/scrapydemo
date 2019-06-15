# -*- coding: utf-8 -*-

import scrapy
from scrapydemo.items import ScrapydemoItem
from scrapy.linkextractors import LinkExtractor
import time

class ScrapydemoSpider(scrapy.Spider):
    name = 'scrapydemo'
    allowed_domains = ['https://www.***.com/']
    start_urls = ['https://www.***.com/']

    def parsemore(self, response):
        # 实例化item
        item = ScrapydemoItem()
        # 注意imgurls是一个集合也就是多张图片
        #item['imgurl'] = response.css(".post img::attr(src)").extract()
        # 抓取文章标题作为图集名称
        #item['imgname'] = response.css(".post-title a::text").extract_first()
        le_two = LinkExtractor(restrict_xpaths='//body/center/div[@id="pages"]/a')
        links = le_two.extract_links(response)
        count = len(links)
        item['imgname'] = response.xpath('/html/body/div[2]/div[2]/p[2]').extract_first()
        item['imgurl'] = response.xpath('//body/div[@class="content"]/center/img/@src').extract()
        item['referer'] = response.url
        yield (item)
        for i in range(count):
            print(links[i].url)
            yield scrapy.Request(links[i].url,callback=self.work,dont_filter=True)



    def work(self,response):
        item = ScrapydemoItem()
        item['imgname'] = response.xpath('/html/body/div[2]/div[2]/p[2]').extract_first()
        item['imgurl'] = response.xpath('//body/div[@class="content"]/center/img/@src').extract()
        item['referer'] = response.url
        yield (item)
        pass


    def parse(self,response):
        le = LinkExtractor(restrict_xpaths='/html/body/div[2]/div[4]/ul/li/a')
        le_list = le.extract_links(response)
        count = len(le_list)
        for i in range(count):
            print(le_list[i-1])
            yield scrapy.Request(le_list[i-1].url,callback=self.parsemore,dont_filter=True)



