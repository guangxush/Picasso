package com.tongji.news.controller;

import com.tongji.common.model.ApiResponse;
import com.tongji.news.model.News;
import com.tongji.news.service.NewsService;
import com.tongji.news.service.impl.MessageServiceConsumer;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * @author: Z
 * @create: 2020/04/17
 */
@RestController
@Slf4j
public class NewsController {

    @Autowired
    NewsService newsService;

    @Autowired
    MessageServiceConsumer consumer;

    /**
     * 增加新闻
     *
     * @param news
     * @return
     */
    @RequestMapping(path = "/insert", method = RequestMethod.POST)
    @ResponseBody
    public ApiResponse<News> insert(@RequestBody News news) {
        News newsVO = newsService.insert(news);
        if (newsVO != null) {
            return new ApiResponse<News>().success(newsVO);
        } else {
            return new ApiResponse<News>().fail(newsVO);
        }
    }

    /**
     * 更新新闻
     *
     * @param news
     * @return
     */
    @RequestMapping(path = "/update", method = RequestMethod.POST)
    @ResponseBody
    public ApiResponse<News> update(@RequestBody News news) {
        News newsVO = newsService.update(news);
        if (newsVO != null) {
            return new ApiResponse<News>().success(newsVO);
        } else {
            return new ApiResponse<News>().fail(newsVO);
        }
    }

    @RequestMapping(path = "/poll", method = RequestMethod.GET)
    @ResponseBody
    public ApiResponse<Boolean> pollData(){
        Boolean result = consumer.consumerNews();
        if (result) {
            return new ApiResponse<Boolean>().success(result);
        } else {
            return new ApiResponse<Boolean>().fail(result);
        }
    }
}

