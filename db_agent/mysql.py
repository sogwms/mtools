import pymysql

from db_agent.abs_col import *

class Mysql(ColFormatA):
    # raw_cols_name 与 hum_cols_name 一一对应
    raw_cols_name = (
        "ORDINAL_POSITION",
        "COLUMN_NAME",
        "DATA_TYPE",
        "COLUMN_COMMENT",
        "COLUMN_DEFAULT",
        "IS_NULLABLE",
        "COLUMN_TYPE",
    )

    hum_cols_name = (
        "pos",
        "name",
        "typePureRaw",
        "comment",
        "default",
        "isNullable",
        "typeRaw",
    )

    sqlText = "SELECT {{columns}} from information_schema.`COLUMNS` WHERE TABLE_NAME = '{table_name}'"

    def __init__(self, host,user,password):
        self.conn = pymysql.connect(host=host,user=user,password=password,db="information_schema",autocommit=True)
        self.cur = self.conn.cursor()

        cols = ""
        for i in self.raw_cols_name:
            cols += i 
            cols += ','
        cols = cols[:-1]
        self.sqlText = self.sqlText.replace("{{columns}}", cols)
        print(self.sqlText)

    def get_col_info_raw(self, table_name):
        self.tableInfo = {}
        self.tableInfo["name"] = table_name
        sql = self.sqlText.format(table_name=table_name)
        self.cur.execute(sql)
        records = self.cur.fetchall()
        return records

    def get_table_info(self):
        return self.tableInfo

    def formatA(self,table_name):
        mapTRawToHum = {
            "varchar":"string",
            "text":"string",
            "varchar":"string",
            "int":"int",
            "datetime":"string",
        }
        mcols = self.get_col_info_in_dict(table_name)
        for col in mcols:
            rawType = col.get('typePureRaw')
            if mapTRawToHum.get(rawType) is None:
                raise Exception('undefined type ref', rawType)
            col["type"] = mapTRawToHum.get(rawType)
        return mcols

    def get_col_info_in_dict(self, table_name):
        cols = self.get_col_info_raw(table_name)
        ret = []
        for col in cols:
            newElem = {}
            for i,v in enumerate(col):
                key = self.hum_cols_name[i]
                newElem[key] = v
            ret.append(newElem)
        return ret

    def __del__(self):
        self.cur.close()
        self.conn.close()
