import sqlite3
import os

class Database():
    def __init__(self,path:str):
        self.db_path = os.path.join(path,"db/db.sqlite")

        con = sqlite3.connect(self.db_path)

        if os.stat(self.db_path).st_size == 0:
            try:
                c = con.cursor()
                c.execute("""CREATE TABLE IF NOT EXISTS Data
                    (id INTEGER PRIMARY KEY, protocol TEXT, url TEXT, data TEXT, lastvisit INTEGER )
                """)
            except Exception as e:
                raise e

    def insert(self,data):
        pass
    
    def select(self,query):
        pass

    