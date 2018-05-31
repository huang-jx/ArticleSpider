# -*- coding: utf-8 -*-
from socket import socket

import scrapy
import re

import time
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import ArticlespiderItem, ArticleItemLoader
from ArticleSpider.pipelines import MysqlPipeline, ArticlespiderPipeline


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobble.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_urls = response.css('#archive .floated-thumb .post-thumb a::attr(href)').extract()
        for post_url in post_urls:
            url = parse.urljoin(response.url, post_url)
            yield Request(url, callback=self.parse_detail, dont_filter=True)
            time.sleep(0.2)
            COOKIES_ENABLED = False
            DOWNLOAD_DELAY = 1

        # 提取下一页的url
        next_urls = response.css('.next.page-numbers::attr(href)').extract_first("")
        if next_urls:
            yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        # 标题
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()
        # 时间
        crttime_content = response.xpath('//div[@class="entry-meta"]/p/text()').extract()
        if len(crttime_content) == 0:
            create_time = 'no'
        else:
            create_time = crttime_content[0].replace('·', '').strip()
        # 文章类别
        article_kind_content = response.xpath('//div[@class="entry-meta"]/p/a/text()').extract()
        if len(article_kind_content) == 0:
            article_kind = 0
        else:
            article_kind = article_kind_content[0]
        # 点赞数
        praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]
        # 收藏数
        fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        match_re = re.match(".*(\d+).*",fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        else:
            fav_nums = 0
        # 评论数
        commant_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_re = re.match(".*(\d+).*", commant_nums)
        if match_re:
            commant_nums = match_re.group(1)
        else:
            commant_nums = 0
        #内容
        # content = response.xpath("//div[@class='entry']").extract()
        # 作者姓名
        author_name_content = response.xpath("//div[@id='author-bio']//a/text()").extract()
        if len(author_name_content) == 0:
            author_name = 'no'
        else:
            author_name = author_name_content[0]

        item_loader = ArticleItemLoader(item=ArticlespiderItem(), response=response)
        item_loader.add_value('url', response.url)
        item_loader.add_xpath('title', '//div[@class="entry-header"]/h1/text()')
        item_loader.add_value('create_time', [create_time])
        item_loader.add_value('article_kind', [article_kind])
        item_loader.add_value('praise_nums', [praise_nums])
        item_loader.add_value('fav_nums', [fav_nums])
        item_loader.add_value('commant_nums', [commant_nums])
       #item_loader.add_value('content', [content])
        item_loader.add_value('author_name', [author_name])
        article_item = item_loader.load_item()
        yield article_item
