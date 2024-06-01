from enum import Enum, unique, Flag
from datetime import datetime, date
from pyspark.sql.functions import to_date

# class SegmentField(Enum):
#     GENDER = 'gender'
#     BIRTHDAY = 'birthday'
#     PLACE  = 'place'
#     TOTAL_PRODUCT_VIEW = 'total_product_view'
#     TOTAL_PURCHASE = 'total_purchase'
#     TOTAL_PURCHASE_VALUE = 'total_purchase_value'
#     AVG_PURCHASE_VALUE = 'total_purchase_value'
#     MIN_PURCHASE_VALUE = 'min_purchase_view'
#     FAVORITE_PRODUCT = 'favorite_products'

# class DataType(Enum):
#     INTEGER = (1, 'integer')
#     LONG = (2, 'long')
#     FLOAT = (3, 'float')
#     TIMESTAMP = (4, 'timestamp')
#     STRING = (5, 'string')
#     DATETIME = (6, 'datetime')
#     BOOLEAN = (7, 'boolean')

#     def __init__(self, value, description):
#         self._value_ = value  # Set the enum value
#         self.description = description  # Set the custom description

#     def __str__(self):
#         return f"{self.name}({self.value}, {self.description})"
    
# class Operator(Enum):
#     EQUAL = (1, 'bằng')
#     GREATER_THAN = (2, 'lớn hơn')
#     LESS_THAN = (3, 'nhỏ hơn')
#     GREATER_OR_EQUAL = (4, 'lớn hơn hoặc bằng')
#     LESS_OR_EQUAL = (5, 'nhỏ hơn hoặc bằng')
#     INCLUDES = (6, 'bao gồm')
#     NOT_EQUAL = (7, 'không bằng')
#     NOT_INCLUDES = (8, 'không bao gồm')

#     def __init__(self, value, description):
#         self._value_ = value  # Set the enum value
#         self.description = description  # Set the custom description

#     def __str__(self):
#         return f"{self.name}({self.value}, {self.description})"

def combile_type (type, value) :
    if type == 'INTEGER' :
        return int(value)
    elif type == 'FLOAT':
        return float(value)
    elif type == 'TIMESTAMP':
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    elif type == 'STRING':
        return str(value)
    elif type == 'DATE':
        return f"to_date('{value}', 'yyyy-MM-dd')"
    elif type == 'BOOLEAN':
        return bool(value)

def combile_operator( segmentField, operator,type, value,):
        if operator == 'EQUAL':
            return f'{segmentField} == {combile_type(type,value)}'
        elif operator == 'GREATER_THAN':
            return f'{segmentField} > {combile_type(type,value)}'
        elif operator == 'LESS_THAN':
            return f'{segmentField} < {combile_type(type,value)}'
        elif operator == 'GREATER_OR_EQUAL':
            return f'({segmentField} > {combile_type(type,value)}) AND ({segmentField} == {combile_type(type,value)})'
        elif operator == 'LESS_OR_EQUAL':
            return f'({segmentField} < {combile_type(type,value)}) AND ({segmentField} == {combile_type(type,value)})'
        elif operator == 'INCLUDES' :
            return f"{segmentField} RLIKE '(^|, ){combile_type(type,value)}($|,)' " # '%compile_type(type,value)%''
        elif operator == 'NOT_EQUAL':
            return f'{segmentField} != {value}'
        elif operator == 'NOT_INCLUDES' :
            return f"{segmentField} NOT RLIKE '(^|, ){combile_type(type,value)}($|,)' "
    

