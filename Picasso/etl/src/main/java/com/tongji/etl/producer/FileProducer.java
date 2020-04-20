package com.tongji.etl.producer;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.tongji.etl.model.JsonNewsData;
import com.tongji.etl.service.FileWatcher;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.LineIterator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.ArrayList;

/**
 * @author: guangxush
 * @create: 2020/04/17
 */
@Service
@Slf4j
@PropertySource("classpath:config/kafka.properties")
public class FileProducer extends KafkaProducer {

    @Resource
    private KafkaTemplate<String, String> kafkaTemplate;

    @Autowired
    private FileWatcher fileWatcher;

    @Value("${kafka.topic:shgx}")
    private String topic;

    private static Gson gson = new GsonBuilder().create();

    /**
     * produce the data from files using fileLineIterator
     * @param fileLineIterators
     */
    @Override
    public void produceFromFile (ArrayList<LineIterator> fileLineIterators){
        for (LineIterator lineIterator : fileLineIterators) {
            while(lineIterator.hasNext()) {
                String line = lineIterator.nextLine();
                // JSON数据: {"id": 74, "label": "113", "title": "在热气球节上迎接第一缕阳光"}
                log.info("+++++++++++++++++++++  message = {}", line);
                JsonNewsData data = fileWatcher.parseFile(line);
                kafkaTemplate.send(topic, data.getId().toString(), line);
            }
        }

    }

    @Override
    public void produceFromService(JsonNewsData[] jsonNewsDataArray) {}

}
