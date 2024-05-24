# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from datetime import datetime, date
import mysql.connector

class TopdevPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline:
    
    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['topdev']
        self.collection = db['job']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Insert item into MongoDB
        self.collection.insert_one(dict(item))
        return item
    
    
    
class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'taolaquanh',    
            database = 'topdev'
        )
        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs(
            id int NOT NULL auto_increment, 
            title TEXT,
            full_address TEXT,
            company_name TEXT,
            detail_url TEXT,
            job_level TEXT,
            skills TEXT,
            job_type TEXT,
            salary TEXT,
            published DATE,
            refreshed DATE,
            PRIMARY KEY (id)
        )
        """)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS companies(
            id int NOT NULL auto_increment, 
            company_name TEXT,
            company_detail_url TEXT,
            company_image_logo TEXT,
            company_industries TEXT,
            PRIMARY KEY (id)
        )
        """)
        
    def process_item(self, item, spider):
       ## Define insert statement
        self.cur.execute("""              
        INSERT INTO jobs (
            title, 
            full_address,
            company_name,
            detail_url,
            job_level,
            skills,
            job_type,
            salary,
            published,
            refreshed 
        ) VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )""", (
            item["title"],
            item["full_address"],
            item["company_name"],
            item["detail_url"],
            item["job_level"],
            item["skills"],
            item["job_type"],
            item["salary"],
            datetime.strptime(item["published"], '%d-%m-%Y').date(),
            datetime.strptime(item["published"], '%d-%m-%Y').date()
        ))
        self.cur.execute("""              
        INSERT INTO companies (
            company_name ,
            company_detail_url,
            company_image_logo ,
            company_industries
        ) VALUES (
            %s,
            %s,
            %s,
            %s
        )""", (
            item["company_name"],
            item["company_detail_url"],
            item["company_image_logo"],
            item["company_industries"],
        ))
        self.conn.commit()    
        return item

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()
        ## Execute insert of data into database
        self.conn.commit()