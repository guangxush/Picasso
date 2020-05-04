package com.tongji.news.repository;

import com.tongji.news.model.News;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * @author: Z
 * @create: 2020/04/17
 */
@Repository
public interface NewsRepo extends JpaRepository<News, Long> {

    Optional<News> findNewsByNewsid(String newsId);

}