# -*- coding: utf-8 -*-
import scrapy


class CrawlzingnewsSpider(scrapy.Spider):
    name = 'zing'
    allowed_domains = ['zingnews.vn']
    start_urls = ['https://zingnews.vn/tan-binh-16-tuoi-duoc-menh-danh-la-my-nam-the-he-moi-cua-yg-post1086753.html']

    def parse(self, response):
        if response.status == 200 and response.css('body::attr("id")').get() == 'page-article':
            print('Crawling from:', response.url)

            all_news = response.css('#page-article')
            for news in all_news:
                yield {
                    'title': news.css('.the-article-title::text').extract(),
                    'author': news.xpath('//*[@id="page-article"]/div[2]/article/header/ul/li[1]/a/text()').extract(),
                    'publish_time': news.css('.the-article-publish::text').extract(),
                    'description': news.css('.the-article-summary::text').extract(),
                    'content': '\n'.join([
                        ''.join(c.css('*::text').getall())
                        for c in news.css('.the-article-body > p')
                    ]),
                    'img_url': news.css('.pic img::attr(src)').extract(),
                    'img_caption': news.css('.caption p::text').extract(),
                    'category': news.css('.parent_cate::text').extract(),
                    'tags': news.xpath('//*[@id="page-article"]/div[8]/article/section[1]/p[2]/strong/text').extract(),
                }

            for href in response.css('a::attr(href)').getall():
                yield response.follow(href, callback=self.parse)

