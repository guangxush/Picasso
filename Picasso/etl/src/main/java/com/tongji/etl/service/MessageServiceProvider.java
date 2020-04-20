package com.tongji.etl.service;

import com.alibaba.dubbo.config.annotation.Service;
import com.tongji.common.service.MessageService;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import java.util.Optional;

/**
 * @author: guangxush
 * @create: 2020/04/20
 */
@Component
@Service(version = "1.0.0", timeout = 3000)
@Slf4j
public class MessageServiceProvider implements MessageService {

    private static final String TOPIC = "news";
    /**
     * receive data from kafka topic
     * @param record
     */
    @KafkaListener(topics = {TOPIC})
    private void listen(ConsumerRecord<?, ?> record) {
        Optional<?> kafkaMessage = Optional.ofNullable(record.value());
        if (kafkaMessage.isPresent()) {
            Object message = kafkaMessage.get();
            log.info("----------------- record = " + record);
            log.info("----------------- message = " + message);
        }
    }

    @Override
    public String sayHello(String name) {
        return "Hello " + name;
    }
}
