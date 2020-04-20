package com.tongji.news.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;

/**
 * @author: Z
 * @create: 2020/04/17
 */
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "news")

public class News {
    /**
     * 新闻表自增id
     */
    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * newsid
     */
    @Column(name = "newsid")
    private String newsid;

    /**
     * 标题
     */
    @Column(name = "title")
    private String title;

    /**
     * 新闻类别
     */
    @Column(name = "category")
    private Long category;
}
