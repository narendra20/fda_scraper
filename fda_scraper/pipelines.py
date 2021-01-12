# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from mysql.connector import errorcode  


class FdaScraperPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'N@rendra2016',
            database = 'fda_database',
            auth_plugin='mysql_native_password'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS fda_rules""")
        self.curr.execute("""create table fda_rules(
                        import_alert text,
                        publication text,
                        type_alert text,
                        description_al text
                        )""")
    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into fda_rules values (%s, %s, %s, %s)""",(
            item['import_alert'],
            item['publication'],
            item['type_alert'],
            item['description_al'],
            # item['charge'][0]
        ))
        self.conn.commit()
