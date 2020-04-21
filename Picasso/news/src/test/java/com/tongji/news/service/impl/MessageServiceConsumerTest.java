package com.tongji.news.service.impl;


import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;


@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
public class MessageServiceConsumerTest {
    @Autowired
    MessageServiceConsumer messageServiceConsumer;

    @Test
    public void testHello(){
        Assert.assertEquals("Hello dubbo", messageServiceConsumer.hello());
        System.out.println(messageServiceConsumer.hello());
    }
}