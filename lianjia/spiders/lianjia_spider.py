# -*- coding: utf-8 -*-

import scrapy
import json
from datetime import date

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    
    
    start_urls = [
        'http://tj.fang.lianjia.com/loupan/heping/',
        'http://tj.fang.lianjia.com/loupan/hedong/',
        'http://tj.fang.lianjia.com/loupan/hexi/',
        'http://tj.fang.lianjia.com/loupan/nankai/',
        'http://tj.fang.lianjia.com/loupan/hebei/',
        'http://tj.fang.lianjia.com/loupan/hongqiao/',
        'http://tj.fang.lianjia.com/loupan/tanggu/',
        'http://tj.fang.lianjia.com/loupan/dongli/',
        'http://tj.fang.lianjia.com/loupan/xiqing/',
        'http://tj.fang.lianjia.com/loupan/jinnan/',
        'http://tj.fang.lianjia.com/loupan/beichen/',
        'http://tj.fang.lianjia.com/loupan/wuqing/',
        'http://tj.fang.lianjia.com/loupan/binhaixinqu/',
        'http://tj.fang.lianjia.com/loupan/kaifaqutj/',
        'http://tj.fang.lianjia.com/loupan/baodi/',
        'http://tj.fang.lianjia.com/loupan/ninghe/',
        'http://tj.fang.lianjia.com/loupan/jinghai/',
        'http://tj.fang.lianjia.com/loupan/jixian/',
    ]

    # def start_requests(self):
    #     url = 'http://tj.fang.lianjia.com/loupan/'
    #     for
        
            
    def parse(self, response):
        if len(response.css('div.fl.l-txt a::attr(href)').extract()) < 4:
            print(response.css('div.fl.l-txt a::attr(href)').extract())
            print('error:', response._url)
            with open('x.html', 'wb') as err:
                err.write(response.body)
            return
        next_url = response.css('div.fl.l-txt a::attr(href)').extract()[3]

        for h in response.css('div.list-wrap div.info-panel'):
            with open(date.today().strftime('%Y_%m_%d')+'.json', 'a', encoding='utf-8') as fp:
                json.dump({
                    '0qu' : response.css('div.fl.l-txt a::text').extract()[3],
                    '1hname' : h.css('div.col-1 a::text').extract_first(),
                    '2hprice' : h.css('div.average span.num::text').extract_first(),
                    '3hsellst' : h.css('div.type span.onsold::text').extract_first(),
                    '4hlive' : h.css('div.type span.live::text').extract_first(),
                    '5haddr' : h.css('div.where span.region::text').extract_first(),
                    '6hlink' : 'http://tj.fang.lianjia.com/loupan/' + h.css('div.col-1 a::attr(href)').extract_first().split("/")[-2],
                }, fp, ensure_ascii=False, sort_keys=True)
                fp.write('\n')

        pagedic = response.css("div.page-box.house-lst-page-box::attr(page-data)").extract()
        if len(pagedic) != 0:
            d = json.loads(pagedic[0])
            if d != None and (d['curPage'] < d['totalPage']):
                npage = response.urljoin(next_url + 'pg'+ str(d['curPage']+1)+'/')
                # print(npage)
                yield scrapy.Request(npage, callback=self.parse)

