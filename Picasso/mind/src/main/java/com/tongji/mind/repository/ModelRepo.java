package com.tongji.mind.repository;

import com.tongji.mind.model.Model;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * @author: guangxush
 * @create: 2020/04/19
 */
@Repository
public interface ModelRepo extends JpaRepository<Model, Long> {
    Optional<Model> findByName(String name);
}
