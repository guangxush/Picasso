package com.tongji.etl.controller;

import com.tongji.etl.model.JsonNewsData;
import com.tongji.etl.producer.PostProducer;
import com.tongji.etl.service.ScheduledTask;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

/**
 * @author: guangxush
 * @create: 2020/04/16
 */
@RestController
@RequestMapping("/kafka")
public class KafkaResource {

    @Autowired
    private PostProducer postProducer;

    @Autowired
    private ScheduledTask scheduledTask;

    /**
     * get the post data and send it to postProducer
     *
     * @param jsonNewsDataArray
     * @return
     */
    @RequestMapping(value = "/producer", method = RequestMethod.POST)
    @ResponseStatus(value = HttpStatus.OK)
    public String postToProduce(@RequestBody JsonNewsData[] jsonNewsDataArray) {
        postProducer.produceFromService(jsonNewsDataArray);
        return "Send Success!!!";
    }

    /**
     * run the task manually
     *
     * @return
     */
    @RequestMapping(value = "/run", method = RequestMethod.POST)
    @ResponseStatus(value = HttpStatus.OK)
    public String postToSendFile() {
        scheduledTask.run();
        return "Task run Success!!!";
    }
}
