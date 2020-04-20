package com.tongji.news.controller;

import com.tongji.common.model.ApiResponse;
import com.tongji.news.model.News;
import com.tongji.news.model.NewsVO;
import com.tongji.news.service.NewsService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import static com.tongji.common.constant.HeadConstant.APP_HEAD;

/**
 * @author: Z
 * @create: 2020/04/17
 */
@RestController
@Slf4j
public class NewsController {

    @Autowired
    NewsService newsService;

//    @Value("${user.school}")
//    private String school;

    /**
     * 增加新闻
     * @param sHead
     * @param news
     * @return
     */
    @RequestMapping(path = "/insert", method = RequestMethod.POST)
    @ResponseBody
    public ApiResponse<NewsVO> insert(@RequestHeader(APP_HEAD) String sHead,
                                        @RequestBody News news){
//        if(!sHead.equals(school)){
//            return new ApiResponse<UserVO>().fail(null);
//        }
        NewsVO newsVO = newsService.insert(news);
        if(newsVO!=null){
            return new ApiResponse<NewsVO>().success(newsVO);
        } else{
            return new ApiResponse<NewsVO>().fail(newsVO);
        }
    }

    /**
     * 更新新闻
     * @param sHead
     * @param news
     * @return
     */
    @RequestMapping(path = "/update", method = RequestMethod.POST)
    @ResponseBody
    public ApiResponse<NewsVO> update(@RequestHeader(APP_HEAD) String sHead,
                                      @RequestBody News news){
//        if(!sHead.equals(school)){
//            return new ApiResponse<UserVO>().fail(null);
//        }
        NewsVO newsVO = newsService.update(news);
        if(newsVO!=null){
            return new ApiResponse<NewsVO>().success(newsVO);
        } else{
            return new ApiResponse<NewsVO>().fail(newsVO);
        }
    }
}

