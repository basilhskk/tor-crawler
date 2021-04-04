import sqlite3
import os
import threading
class Database():
    lock = threading.Lock()

    def __init__(self,path:str):
        self.db_path = os.path.join(path,"db/db.sqlite")

        try:
            con = sqlite3.connect(self.db_path, check_same_thread=False)
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
        c=None
        con=None
        try:
            with Database.lock:
                con = sqlite3.connect(self.db_path, check_same_thread=False)

                c = con.cursor()
                c.execute(f"""INSERT INTO Data (protocol,url,data,lastvisit) VALUES ("{data['protocol']}","{data['url']}","{data['data']}",{data['lastvisit']}) """)
                con.commit()
        except Exception as e:
            raise e
        finally:
            if c :
                c.close()
            if con:
                con.close()

    def update(self,data:dict):
        c=None
        con=None
        try:
            with Database.lock:
                con = sqlite3.connect(self.db_path, check_same_thread=False)
                c = con.cursor()
                c.execute(f"""UPDATE Data SET protocol="{data['protocol']}", data="{data['data']}", lastvisit="{data['lastvisit']}" WHERE url="{data['url']}" """)
                con.commit()
                c.close()
        except Exception as e:
            raise e
        finally:
            if c :
                c.close()
            if con:
                con.close()

    def isCrawled(self,url:str) -> list:
        c=None
        con=None
        try:
            con = sqlite3.connect(self.db_path, check_same_thread=False)
        
            c = con.cursor()
            c.execute(f"""SELECT url from Data WHERE url = '{url}' and lastvisit != 0 """)
            rows = c.fetchall()
            c.close()

            return rows

        except Exception as e:
            raise e
        finally:
            if c :
                c.close()
            if con:
                con.close()


    def query(self,query:str) -> list:
        c=None
        con=None
        try:
            con = sqlite3.connect(self.db_path, check_same_thread=False)
       
            c = con.cursor()
            c.execute(query)
            rows = c.fetchall()
            c.close()

            return rows

        except Exception as e:
            raise e
        finally:
            if c :
                c.close()
            if con:
                con.close()


    