package com.tongji.common.service;

import java.util.Map;

/**
 * @author: guangxush
 * @create: 2020/04/20
 */
public interface MessageService {

    /**
     * test method
     * @param name
     * @return
     */
    String sayHello(String name);

    Map<String, String> getMessage();
}
