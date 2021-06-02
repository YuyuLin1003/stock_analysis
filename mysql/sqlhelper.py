import pymysql
import os
from dbutils.pooled_db import PooledDB
import time

from dotenv import load_dotenv

load_dotenv(verbose=True)



class MySQLHelper(object):
    def __init__(self):
        while True:
            host= os.environ.get("SQL_HOST")
            port= int(os.environ.get("SQL_PORT"))
            db= os.environ.get("SQL_DB")
            password= os.environ.get("SQL_PASSWORD")
            user= os.environ.get("SQL_USER")
            print("host is {}".format(host))
            self.pool = PooledDB(pymysql,
                                5,
                                host=host,
                                user=user,
                                passwd=password,
                                db=db,
                                port=port)
            if self.pool:
                print('mysql connect success')
                break
            print('connect fail,retry in 5 seconds')
            time.sleep(5)
    # get one connection from pool
    def get_conn(self):
        conn = self.pool.connection()
        cur = conn.cursor()
        return conn, cur
    # close connection
    def close_conn(self,conn,cur):
        cur.close()
        conn.close()

    def deal_with_sql(self,cur,conn,SQL, types='SELECT'):
        if types == 'SELECT':
            cur.execute(SQL)
            result = cur.fetchall()
            return result
        elif types == 'INSERT':
            try:
                cur.execute(SQL)
                conn.commit()
                return True
            except BaseException as e:
                print("INSERT FAIL: ",e)
                return False
        elif types == 'UPDATE':
            try:
                cur.execute(SQL)
                conn.commit()
                return True
            except BaseException as e:
                print('UPDATE FAIL: ',e)
                return False
        elif types == 'DELETE':
            try:
                cur.execute(SQL)
                conn.commit()
                return True
            except BaseException as e:
                print('DELETE FAIL: ',e)
                return False
        else:
            return None


mySQLHelper = MySQLHelper()

def getSQLHelper():
    return mySQLHelper        
if __name__ == '__main__':
    mydb=MySQLHelper()
    (conn,cur) = mydb.get_conn()
    result = mydb.deal_with_sql(cur,conn,"SELECT * FROM `markit`; ",'SELECT')
    print(result) 