from enum import Enum, unique, Flag

class SegmentField(Enum):
    GENDER = 'gender'
    BIRTHDAY = 'birthday'
    PLACE  = 'place'
    TOTAL_PRODUCT_VIEW = 'total_product_view'
    TOTAL_PURCHASE = 'total_purchase'
    TOTAL_PURCHASE_VALUE = 'total_purchase_value'
    AVG_PURCHASE_VALUE = 'total_purchase_value'
    MIN_PURCHASE_VALUE = 'min_purchase_view'
    FAVORITE_PRODUCT = 'favorite_products'

class DataType(Enum):
    INTEGER = (1, 'integer')
    LONG = (2, 'long')
    FLOAT = (3, 'float')
    TIMESTAMP = (4, 'timestamp')
    STRING = (5, 'string')
    DATETIME = (6, 'datetime')
    BOOLEAN = (7, 'boolean')

    def __init__(self, value, description):
        self._value_ = value  # Set the enum value
        self.description = description  # Set the custom description

    def __str__(self):
        return f"{self.name}({self.value}, {self.description})"
    
class Operator(Enum):
    EQUAL = (1, 'bằng')
    GREATER_THAN = (2, 'lớn hơn')
    LESS_THAN = (3, 'nhỏ hơn')
    GREATER_OR_EQUAL = (4, 'lớn hơn hoặc bằng')
    LESS_OR_EQUAL = (5, 'nhỏ hơn hoặc bằng')
    INCLUDES = (6, 'bao gồm')
    NOT_EQUAL = (7, 'không bằng')
    NOT_INCLUDES = (8, 'không bao gồm')

    def __init__(self, value, description):
        self._value_ = value  # Set the enum value
        self.description = description  # Set the custom description

    def __str__(self):
        return f"{self.name}({self.value}, {self.description})"

    
    
    

