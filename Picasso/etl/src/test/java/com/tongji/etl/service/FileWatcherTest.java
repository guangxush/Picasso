package com.tongji.etl.service;

import com.tongji.etl.model.JsonNewsData;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import static org.junit.Assert.assertEquals;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
public class FileWatcherTest {

    @Autowired
    private FileWatcher fileWatcher;

    @Test
    public void testparseFile(){
        String line = "{\"id\": 74, \"label\": \"113\", \"title\": \"在热气球节上迎接第一缕阳光\"}";
        JsonNewsData message = fileWatcher.parseFile(line);
        assertEquals(new Long("74"), message.getId());
        assertEquals("在热气球节上迎接第一缕阳光", message.getTitle());
        assertEquals("113", message.getLabel());
    }
}