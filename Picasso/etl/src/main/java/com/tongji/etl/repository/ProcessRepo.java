package com.tongji.etl.repository;

import com.tongji.etl.model.Process;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * @author: guangxush
 * @create: 2020/04/18
 */
@Repository
public interface ProcessRepo extends JpaRepository<Process, Long> {

    @Query(value = "select distinct * from process where processed = 0", nativeQuery = true)
    List<Process> queryUnprocessedRecords();

    Optional<Process> findProcessByDate(String date);
}
