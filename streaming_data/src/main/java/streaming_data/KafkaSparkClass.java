package streaming_data;

// import org.apache.spark.sql.Dataset;
// import org.apache.spark.sql.Row;
// import org.apache.spark.sql.SparkSession;
// import org.apache.spark.sql.functions;
// import org.apache.spark.sql.streaming.StreamingQuery;
// import org.apache.spark.sql.types.StructType;

// import static org.apache.spark.sql.functions.*;

import java.util.Collection;
import java.util.Collections;

import org.apache.spark.streaming.Duration;
// import org.apache.spark.streaming.api.java.JavaDStream;
import org.apache.spark.streaming.api.java.JavaInputDStream;
// import org.apache.spark.streaming.api.java.JavaPairInputDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;
import org.apache.spark.streaming.kafka010.ConsumerStrategies;
import org.apache.spark.streaming.kafka010.KafkaUtils;
import org.apache.spark.streaming.kafka010.LocationStrategies;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

// import scala.runtime.BoxedUnit;

// import org.apache.commons.codec.StringDecoder;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
// import org.apache.spark.api.java.function.ForeachPartitionFunction;
// import org.apache.spark.api.java.function.VoidFunction2;
// import org.apache.spark.network.protocol.Encoders;

// import java.sql.Struct;
import java.util.ArrayList;
// import java.util.Arrays;
// import java.util.Collection;
import java.util.HashMap;
// import java.util.Iterator;
import java.util.List;
import java.util.Map;
// import java.util.Set;

public class KafkaSparkClass {
    public static void main(String[] args) throws InterruptedException {
        ObjectMapper objectMapper = new ObjectMapper();
        Schema schema = new Schema();
        System.out.println("Start Spark Streaming.... ");
        SparkConf conf = new SparkConf().setMaster("spark://172.25.0.3:7077").setAppName("event_treaming");
        JavaSparkContext sc = new JavaSparkContext(conf);
        // batch Duration- the time interval at which streaming data will be divided
        // into batches
        JavaStreamingContext ssc = new JavaStreamingContext(sc, new Duration(1000));
        Map<String, Object> kafkaParams = new HashMap<>();
        kafkaParams.put("bootstrap.servers", KafkaConfig.BOOTSTRAP_SERVERS);
        Collection<String> topics = Collections.singleton(KafkaConfig.TOPIC_NAME);

        JavaInputDStream<ConsumerRecord<String, String>> directKafkaStream = KafkaUtils.createDirectStream(
                ssc,
                LocationStrategies.PreferConsistent(),
                ConsumerStrategies.<String, String>Subscribe(topics, kafkaParams));

        List<String> allRecord = new ArrayList<String>();

        final String COMMA = ",";

        directKafkaStream.foreachRDD(rdd -> {
            rdd.foreach(record -> {
                try {
                    JsonNode jsonNode = objectMapper.readTree(record.value());
                    System.out.println("Record: " + jsonNode.toString());
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });
        });

        // JavaPairInputDStream<String, String> directKafkaStream =
        // KafkaUtils.createDirectStream(
        // ssc,
        // String.class,
        // String.class,
        // StringDecoder.class,
        // StringDecoder.class,
        // kafkaParams,
        // topics);

        // ConsumerStrategies.Subscribe(topics, kafkaParams));
        // Schema schema = new Schema();

        // SparkSession spark = SparkSession.builder()
        // .appName("event_treaming")
        // .getOrCreate();

        // Dataset<Row> df = spark
        // .readStream()
        // .format("kafka")
        // .option("kafka.bootstrap.servers", KafkaConfig.BOOTSTRAP_SERVERS)
        // .option("subscribe", KafkaConfig.TOPIC_NAME)
        // .load();

        // Dataset<Row> jsonDF = df.selectExpr("CAST(value AS STRING)")
        // .select(functions.from_json(functions.col("value"),
        // schema.eventSchema).as("data"))
        // .select("data.*");
        // jsonDF.show();

        // // Tạo một ForeachPartitionFunction tùy chỉnh để ghi dữ liệu vào
        // Elasticsearch
        // ForeachPartitionFunction<Row> foreachPartitionFunction = new
        // ForeachPartitionFunction<Row>() {
        // @Override
        // public void call(Iterator<Row> partition) throws Exception {
        // // Lặp qua mỗi phần tử trong partition
        // while (partition.hasNext()) {
        // Row row = partition.next();
        // // Ghi dữ liệu vào Elasticsearch ở đây
        // // (Bạn cần thêm mã để ghi dữ liệu vào Elasticsearch)
        // }
        // }
        // };

        // // Ghi dữ liệu vào Elasticsearch bằng foreachBatch
        // jsonDF.writeStream()
        // .foreachBatch(new ForeachBatchFunction<Row>() {
        // @Override
        // public void call(Dataset<Row> batchDF, long batchId) throws Exception {
        // // Lặp qua mỗi partition trong batch và gọi hàm foreachPartitionFunction
        // batchDF.foreachPartition(foreachPartitionFunction);
        // }
        // })
        ssc.start();
        ssc.awaitTermination();

    }
}
