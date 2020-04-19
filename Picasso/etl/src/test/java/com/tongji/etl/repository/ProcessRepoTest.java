package com.tongji.etl.repository;

import junit.framework.TestCase;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
public class ProcessRepoTest extends TestCase {

    @Autowired
    ProcessRepo processRepo;

    @Test
    public void testQueryLastRecord() {
        System.out.println(processRepo.queryUnprocessedRecords().get(0).getDate());
    }
}