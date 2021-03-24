import sqlite3
import os

class Database():
    def __init__(self,path:str):
        self.db_path = os.path.join(path,"db/db.sqlite")

        try:
            con = sqlite3.connect(self.db_path)
        except:
            os.touch(self.db_path)
            
        if os.stat(self.db_path).st_size == 0:
            try:
                c = con.cursor()
                c.execute("""CREATE TABLE IF NOT EXISTS Data
                    ( protocol TEXT, url TEXT PRIMARY KEY UNIQUE, data TEXT, lastvisit INTEGER )
                """)
            except Exception as e:
                raise e

    def insert(self,data:dict):
        try:
            con = sqlite3.connect(self.db_path)
        except Exception as e:
            raise e

        try:
            c = con.cursor()
            c.execute(f"""INSERT INTO Data (protocol,url,data,lastvisit) VALUES ("{data['protocol']}","{data['url']}","{data['data']}",{data['lastvisit']}) """)
            con.commit()
            c.close()
        except Exception as e:
            raise e

    def select(self,url:str):
        try:
            con = sqlite3.connect(self.db_path)
        except Exception as e:
            raise e

        try:
            c = con.cursor()
            c.execute(f"""SELECT url from Data WHERE url = '{url}' """)
            rows = c.fetchall()
            c.close()

            return rows

        except Exception as e:
            raise e


    