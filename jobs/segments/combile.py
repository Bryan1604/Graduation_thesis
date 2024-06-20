from enum import Enum, unique, Flag
from datetime import datetime, date
from pyspark.sql.functions import to_date

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
    

