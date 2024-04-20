package streaming_data;

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

public class App {
    // static KafkaSparkClass kafkaSparkClass = new KafkaSparkClass();

    public static void main(String[] args) {
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
    }
}
