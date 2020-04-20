package com.tongji.news.service.impl;

import com.alibaba.dubbo.config.annotation.Reference;
import com.tongji.common.service.MessageService;
import org.springframework.stereotype.Component;

/**
 * @author: guangxush
 * @create: 2020/04/20
 */
@Component
public class MessageServiceConsumer {

    @Reference(version = "1.0.0", timeout = 3000)
    private MessageService messageService;

    public String hello() {
        String name = "dubbo";
        return messageService.sayHello(name);
    }
}
