package com.tongji.news.service.impl;

import com.tongji.common.exception.ApiInternalError;
import com.tongji.news.model.News;
import com.tongji.news.repository.NewsRepo;
import com.tongji.news.service.NewsService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

/**
 * @author: Z
 * @create: 2020/04/17
 */
@Service
@Slf4j
public class NewsServiceImpl implements NewsService {

    @Autowired
    private NewsRepo newsRepo;

    @Override
    public News insert(News news) {
        News newsVO;
        String newsNid = news.getNewsid();
        if (newsNid == null) {
            log.error("news id is null");
            throw new ApiInternalError("news id is null, news info:{}", news.toString());
        }
        Optional<News> newsInDb = newsRepo.findNewsByNewsid(news.getNewsid());
        try {
            if (newsInDb.isPresent()) {
                //更新操作
                if (newsNid.equals(newsInDb.get().getNewsid())) {
                    //新闻已添加
                    log.error("This newsid has been used!");
                    return null;
                }
            }
            //插入操作
            newsVO = saveNews(news);
        } catch (Exception e) {
            return null;
        }
        return newsVO;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public News update(News news) {
        News newsInDB;
        String newsNewsid = news.getNewsid();
        if (newsNewsid == null) {
            log.error("news id is null");
            throw new ApiInternalError("news id is null, news info:{}", news.toString());
        }
        Optional<News> newsInDb = newsRepo.findNewsByNewsid(news.getNewsid());
        try {
            if (newsInDb.isPresent()) {
                if (!newsNewsid.equals(newsInDb.get().getNewsid())) {
                    //账号未注册过
                    log.error("This newsid has not been used!");
                    throw new ApiInternalError("This newsid {} has not been used!", news.getNewsid());
                }
            }
            //更新操作
            news.setId(newsInDb.get().getId());
            newsInDB = saveNews(news);
        } catch (Exception e) {
            return null;
        }
        return newsInDB;
    }

    /**
     * 保存用户信息
     *
     * @param news
     * @return
     */
    private News saveNews(News news) {
        news = newsRepo.save(news);
        if (news.getId() <= 0) {
            log.error("fail to save the news:{}", news.toString());
            throw new ApiInternalError("fail to save the news:{}", news.toString());
        }
        return News.builder().newsid(news.getNewsid()).title(news.getTitle()).build();
    }
}
