from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType



schema_event = StructType([
    StructField("event_id", StringType(), True),
    StructField("time", StringType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("domain_userid", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("products", ArrayType(
        StructType([
            StructField("product_id", IntegerType(), True),
            StructField("product_name", StringType(), True),
            StructField("price", IntegerType(), True),
            StructField("quantity", IntegerType(), True),
            StructField("category_id", IntegerType(), True)
        ])
    ), True)
])

