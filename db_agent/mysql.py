import pymysql

class Mysql:

    raw_cols_name = (
        "ORDINAL_POSITION",
        "COLUMN_NAME",
        "DATA_TYPE",
        "COLUMN_DEFAULT",
        "COLUMN_COMMENT",
        "IS_NULLABLE",
        "COLUMN_TYPE",
    )

    hum_cols_name = (
        "pos",
        "name",
        "type",
        "default",
        "comment",
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

    def get_col_info(self, table_name):
        self.cur.execute(self.sqlText.format(table_name= table_name))
        records = self.cur.fetchall()
        return records

    def get_col_info_raw(self, table_name):
        self.cur.execute(self.sqlText.format(table_name= table_name))
        records = self.cur.fetchall()
        return records

    def get_col_info_in_dict(self, table_name):
        cols = self.get_col_info_raw(table_name)
        ret = [{}]
        for col in cols:
            newElem = {}
            print(col)
            for i,v in enumerate(col):
                key = self.hum_cols_name[i]
                newElem[key] = v
            ret.append(newElem)
        return ret

    def __del__(self):
        self.cur.close()
        self.conn.close()
