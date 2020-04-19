package com.tongji.etl.consumer;

import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import java.util.Optional;

/**
 * @author: guangxush
 * @create: 2020/04/18
 */
@Component
@Slf4j
public class KafkaReceiver {

    private static final String TOPIC = "news";
    /**
     * receive data from kafka topic
     * @param record
     */
    @KafkaListener(topics = {TOPIC})
    public void listen(ConsumerRecord<?, ?> record) {

        Optional<?> kafkaMessage = Optional.ofNullable(record.value());

        if (kafkaMessage.isPresent()) {
            Object message = kafkaMessage.get();
            log.info("----------------- record =" + record);
            log.info("----------------- message =" + message);
        }
    }
}
