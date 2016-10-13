# -*- coding: utf-8 -*-

import scrapy
import json

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    
    
    start_urls = [ 'http://tj.fang.lianjia.com/loupan/' ]
        
            
    def parse(self, response):
        #page = response.url.split("/")[-2]
#        filename = 'loupan.html'
#        with open(filename, 'wb') as f:
#            f.write(response.body)
#        self.log('Saved file %s' % filename)
        
        for h in response.css('div.list-wrap div.info-panel'):
            yield {
                   'hname' : h.css('div.col-1 a::text').extract_first(),
                   'hprice' : h.css('div.average span.num::text').extract_first(),
                   'hsellst' : h.css('div.type span.onsold::text').extract_first(),
                   'hlive' : h.css('div.type span.live::text').extract_first(),
                   'haddr' : h.css('div.where span.region::text').extract_first(),
                   'hlink' : self.start_urls[0] + h.css('div.col-1 a::attr(href)').extract_first().split("/")[-2],
                   }
                  
        d = json.loads(response.css("div.page-box.house-lst-page-box::attr(page-data)").extract_first())
        if d['curPage'] < d['totalPage']:
            npage = response.urljoin('/loupan/pg'+str(d['curPage']+1)+'/')
            yield scrapy.Request(npage, callback=self.parse)