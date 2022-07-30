# 接口定义， 将col 转换为特定(标准)形式

from abc import ABCMeta,abstractmethod

class TableInfo(metaclass=ABCMeta):
    @abstractmethod
    def get_table_info(self):
        pass

class ColFormatA(TableInfo,metaclass=ABCMeta):
    """
    table:
        name <raw>
    columns:
        pos <raw>
        name <raw>
        type <map> (ops: int,string,bool)
        comment <raw>
        default <raw>
        isNullable <TF>
        typePureRaw <raw>
        typeRaw <raw>
    """
    @abstractmethod
    def formatA(self):
        pass