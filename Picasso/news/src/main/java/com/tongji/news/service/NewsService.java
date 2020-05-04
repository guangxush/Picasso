package com.tongji.news.service;

import com.tongji.news.model.News;
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
    News insert(News news);

    /**
     * 修改新闻信息
     * @param news
     * @return
     */
    News update(News news);

    /**
     * 查询新闻信息
     * @param nid
     * @return
     */
    String queryNewsFromRedis(String nid);
}
