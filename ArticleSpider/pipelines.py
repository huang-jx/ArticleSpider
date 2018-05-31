# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item
class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '888888', 'spider_db', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(url, title, create_time, article_kind, praise_nums, fav_nums, 
            commant_nums, author_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["url"], item["title"], item["create_time"], item["article_kind"], item["praise_nums"], item["fav_nums"], item["commant_nums"], item["author_name"]))
        self.conn.commit()