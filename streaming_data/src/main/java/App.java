import java.util.Arrays;

import org.apache.spark.SparkConf;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.streaming.DataStreamReader;
import org.apache.spark.sql.streaming.StreamingQuery;
import org.apache.spark.sql.streaming.StreamingQueryException;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.StructType;

public class App {
    public static void main(String[] args) {
        // Tạo một SparkSession
        SparkSession spark = SparkSession
                .builder()
                .appName("streaming_event")
                .master("local[*]") // Chỉ định master URL
                .getOrCreate();

        // Đọc dữ liệu từ Kafka vào DataFrame
        Dataset<Row> kafkaDF = spark
                .readStream()
                .format("kafka")
                .option("kafka.bootstrap.servers", "localhost:29092")
                .option("subscribe", "enriched")
                .load();
        kafkaDF.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)");
        // Hiển thị schema của DataFrame
        kafkaDF.printSchema();

        // Thực hiện các thao tác xử lý dữ liệu khác ở đây

        // Khởi chạy xử lý streaming và chờ kết thúc
        try {
            spark.streams().awaitAnyTermination();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
