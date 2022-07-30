from db_agent import mysql
from jinja2 import Template

def t2():
    m = mysql.Mysql("localhost", "root", "root")
    cols = m.formatA("collection")
    # m.get_col_info_in_dict("collection")

    return cols,m.get_table_info()

def t3(cols,talbeInfo,filename):
    tpl = ""
    with open("template/"+filename) as f:
        tpl = f.read()
    template = Template(tpl)
    final = template.render(array=('John dan','Vano'), cols=cols,table=talbeInfo)
    print(final)

if __name__ == "__main__":
    print("start")
    # t2()
    cols, table = t2()
    t3(cols,table,"go-gorm.jinja2")
    # m = mysql.Mysql("localhost", "root", "root")
    # m.formatA("collection")
