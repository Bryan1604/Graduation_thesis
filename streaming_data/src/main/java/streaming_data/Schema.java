package streaming_data;

import org.apache.spark.sql.types.ArrayType;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.StructType;

public class Schema {
    StructType productSchema = new StructType()
            .add("product_id", DataTypes.IntegerType)
            .add("product_name", DataTypes.StringType)
            .add("price", DataTypes.IntegerType)
            .add("quantity", DataTypes.IntegerType)
            .add("category_id", DataTypes.IntegerType);
    ArrayType products = DataTypes.createArrayType(productSchema);

    // define event schema
    StructType eventSchema = new StructType()
            .add("event_id", DataTypes.IntegerType)
            .add("time", DataTypes.StringType) // TODO: kiem tra lai nen de la timeDataTypes hay StringType
            .add("user_id", DataTypes.IntegerType)
            .add("domain_userid", DataTypes.StringType)
            .add("evetn_type", DataTypes.StringType)
            .add("products", products);

}