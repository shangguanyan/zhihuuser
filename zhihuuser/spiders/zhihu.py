# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Spider


class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['https://www.zhihu.com/']
    start_urls = ['https://www.zhihu.com//']

    start_user = 'guo-zi-501'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'

    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
    def start_requests(self):
        yield scrapy.Request(self.user_url.format(user = self.start_user,include=self.user_query),callback=self.parse_user,dont_filter=True)
        yield scrapy.Request(self.followers_url.format(user = self.start_user,include=self.followers_query,offset=0,limit=20),callback = self.parse_follower,dont_filter=True)

    def parse_user(self, response):
        result = json.loads(response.text)
        from ..items import UserItem
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item

        yield scrapy.Request(self.followers_url.format(user = result.get('url_token'),include=self.followers_query,offset=0,limit=20)
                      , callback=self.parse_follower,dont_filter=True)

    def parse_follower(self,response):
        results = json.loads(response.text)
        print(results)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),
                              callback=self.parse_user,dont_filter=True)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield scrapy.Request(url=next_page,callback=self.parse_follower,dont_filter=True)
