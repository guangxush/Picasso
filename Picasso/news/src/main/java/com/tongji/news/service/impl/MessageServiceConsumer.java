package com.tongji.news.service.impl;

import com.alibaba.dubbo.config.annotation.Reference;
import com.alibaba.fastjson.JSONObject;
import com.tongji.common.model.JsonNewsData;
import com.tongji.common.service.MessageService;
import com.tongji.news.model.News;
import com.tongji.news.service.NewsService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;

import java.util.Map;

/**
 * @author: guangxush
 * @create: 2020/04/20
 */
@Component
@Slf4j
public class MessageServiceConsumer {

    @Reference(version = "1.0.0", timeout = 3000)
    private MessageService messageService;

    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    @Autowired
    private NewsService newsService;

    public String hello() {
        String name = "dubbo";
        return messageService.sayHello(name);
    }

    public boolean consumerNews() {
        Map<String, String> messageMap = messageService.getMessage();
        int messageCount = messageMap.size();
        for (String key : messageMap.keySet()) {
            JsonNewsData json = parseFile(messageMap.get(key));
            News news = News.builder().newsid(key).category(json.getLabel()).title(json.getTitle()).build();
            //存入Redis中
            stringRedisTemplate.opsForValue().set(key, json.getTitle());
            if (newsService.insert(news) != null) {
                log.info("news {} has been insert into db.", news.getNewsid());
                messageCount--;
            }
        }
        return messageCount == 0;
    }

    /**
     * parse the data file and load data into SchemaData
     *
     * @param line
     * @return SchemaData
     * {"id": 74, "label": "113", "title": "在热气球节上迎接第一缕阳光"}
     */
    private JsonNewsData parseFile(String line) {
        JSONObject jsonObject = (JSONObject) JSONObject.parse(line);
        return JsonNewsData.builder()
                .id(jsonObject.getLong("id"))
                .label(jsonObject.getLong("label"))
                .title(jsonObject.getString("title"))
                .build();
    }
}
