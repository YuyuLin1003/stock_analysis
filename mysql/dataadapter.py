import mysql.sqlhelper as sqlhelper
from datetime import date
import logging


SQLHelper = sqlhelper.getSQLHelper()

dateFmt = "%Y-%m-%d"
UPDATE_FINISH_STR="Update Finished"
class MarkitDataHelper(object):
    def __init__(self):
        (self.conn,self.cur) = SQLHelper.get_conn()
    
    def getCDX_NA_HY(self):
        sql = "SELECT label,value,date FROM `markit` where label = 'CDX.NA.HY';"
        result = SQLHelper.deal_with_sql(self.cur,self.conn,sql)
        return result

    def getCDX_NA_IG(self):
        sql = "SELECT label,value,date FROM `markit` where label = 'CDX.NA.IG';"
        result = SQLHelper.deal_with_sql(self.cur,self.conn,sql)
        return result

    def insertTodayIGData(self,value):
        today = date.today().strftime(dateFmt)
        sql = "SELECT * FROM `markit` where label = 'CDX.NA.IG' AND date = '{}';".format(today)
        result = SQLHelper.deal_with_sql(self.cur,self.conn,sql)
        if len(result) == 0:
            sql = "INSERT INTO `markit`(`label`, `value`, `date`) VALUES\
            ('CDX.NA.IG', {}, '{}');".format(value,today)
            result= SQLHelper.deal_with_sql(self.cur,self.conn,sql,types='INSERT')
        else:
            logging.info("Today CDX.IG Data is already presented.")            
            return UPDATE_FINISH_STR
        return True if result is True else False

    def insertTodayHYData(self,value):
        today = date.today().strftime(dateFmt)
        sql = "SELECT * FROM `markit` where label = 'CDX.NA.HY' AND date = '{}';".format(today)
        result = SQLHelper.deal_with_sql(self.cur,self.conn,sql)
        if len(result) == 0:
            sql = "INSERT INTO `markit`(`label`, `value`, `date`) VALUES\
            ('CDX.NA.HY', {}, '{}');".format(value,today)
            result= SQLHelper.deal_with_sql(self.cur,self.conn,sql,types='INSERT')
        else:
            logging.info("Today CDX.HY Data is already presented.")            
            return UPDATE_FINISH_STR
        return True if result is True else False

    


if __name__ =='__main__':
    adapter=MarkitDataHelper()
    print(adapter.insertTodayIGData(22))