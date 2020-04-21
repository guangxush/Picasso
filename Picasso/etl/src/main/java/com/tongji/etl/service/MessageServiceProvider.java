package com.tongji.etl.service;

import com.alibaba.dubbo.config.annotation.Service;
import com.tongji.common.service.MessageService;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

/**
 * @author: guangxush
 * @create: 2020/04/20
 */
@Component
@Service(version = "1.0.0", timeout = 3000)
// 注意不要随便使用@Slf4j,版本不一致可能会出现冲突
public class MessageServiceProvider implements MessageService {

    private static final String TOPIC = "news";

    private static Map<String, String> map = new ConcurrentHashMap<>();

    /**
     * receive data from kafka topic
     *
     * @param record
     */
    @KafkaListener(topics = {TOPIC})
    private void listen(ConsumerRecord<?, ?> record) {
        Optional<?> kafkaMessage = Optional.ofNullable(record.value());
        if (kafkaMessage.isPresent()) {
            String message = kafkaMessage.get().toString();
            System.out.println("----------------- record = " + record);
            if (record.key() == null) {
                return;
            }
            String key = record.key().toString();
            map.put(key, message);
            System.out.println("----------------- message = " + message);
        }
    }

    @Override
    public Map<String, String> getMessage() {
        return map;
    }

    @Override
    public String sayHello(String name) {
        return "Hello " + name;
    }
}
