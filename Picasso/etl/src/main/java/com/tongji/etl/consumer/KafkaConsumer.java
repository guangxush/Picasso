package com.tongji.etl.consumer;

import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;

/**
 * @author: guangxush
 * @create: 2020/04/19
 */
public class KafkaConsumer {

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;


    public void consumer(){

    }
}
