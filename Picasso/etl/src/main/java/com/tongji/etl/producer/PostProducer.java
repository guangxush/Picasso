package com.tongji.etl.producer;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.tongji.etl.model.JsonNewsData;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.LineIterator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.util.ArrayList;

/**
 * @author: guangxush
 * @create: 2020/04/17
 */
@Service
@Slf4j
@PropertySource("classpath:config/kafka.properties")
public class PostProducer extends KafkaProducer {

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    private static Gson gson = new GsonBuilder().create();

    @Value("${kafka.topic}")
    private String topic;

    /**
     * produce the data from web services
     * @param jsonNewsDataArray
     */
    @Override
    public void produceFromService(JsonNewsData[] jsonNewsDataArray) {
        for (JsonNewsData message : jsonNewsDataArray) {
            log.info("+++++++++++++++++++++  message = {}", gson.toJson(message));
            kafkaTemplate.send(topic, gson.toJson(message));
        }
    }

    @Override
    public void produceFromFile(ArrayList<LineIterator> fileLineIterators) {}
}
