from db_agent import mysql
from jinja2 import Template

def t2():
    m = mysql.Mysql("localhost", "root", "root")
    cols = m.get_col_info_in_dict("collection")
    # for i in cols:
    #     print(i)
    # cols = m.get_col_info("tag")
    # for i in cols:
    #     print(i)
    return cols

def t3(cols):
    tmpl = """{#- note:for trim space only -#}
{% for col in cols -%}
    {{ col.name }} {{col.type}} `gorm:"column:{{col.name}};default:{{col.default}}" json:"{{col.name}}"` // {{col.comment}}
{% endfor -%}
"""
    template = Template(tmpl)
    final = template.render(array=('John dan','Vano'), cols=cols)
    print(final)

if __name__ == "__main__":
    print("start")
    t3(t2())
