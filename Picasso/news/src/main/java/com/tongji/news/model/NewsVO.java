package com.tongji.news.model;


import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;


/**
 * @author: Z
 * @create: 2020/04/17
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class NewsVO {
    /**
     * 新闻表自增id
     */
    private Long id;

    /**
     * newsid
     */
    private String newsid;

    /**
     * 标题
     */
    private String title;

    /**
     * 新闻类别
     */
    private Long category;
}
