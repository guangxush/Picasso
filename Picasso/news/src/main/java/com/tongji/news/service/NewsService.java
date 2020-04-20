package com.tongji.news.service;

import com.tongji.news.model.News;
import com.tongji.news.model.NewsVO;
/**
 * @author: Z
 * @create: 2020/04/17
 */
public interface NewsService {
    /**
     * 新增新闻
     * @param news
     * @return
     */
    NewsVO insert(News news);

    /**
     * 修改新闻信息
     * @param news
     * @return
     */
    NewsVO update(News news);
}
