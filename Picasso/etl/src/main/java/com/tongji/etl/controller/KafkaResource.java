package com.tongji.etl.controller;

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
//    @Autowired
//    private PostProducer postProducer;

    /**
     * get the post data and send it to postProducer
     * @param schemaDataArray
     * @return
     */
//    @RequestMapping(value = "/producer", method = RequestMethod.POST)
//    @ResponseStatus(value = HttpStatus.OK)
//    public String postToProduce (@RequestBody SchemaData[] schemaDataArray) {
//        postProducer.produceFromService(schemaDataArray);
//        return "Send Success!!!";
//    }
}
