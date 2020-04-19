package com.tongji.etl.producer;

import org.apache.commons.io.LineIterator;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.concurrent.ExecutionException;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
public class FileProducerTest {

    @Autowired
    private FileProducer fileProducer;

    @Test
    public void testProducer() throws InterruptedException, ExecutionException, IOException {
        String msg1 = "{\"id\": 74, \"label\": \"113\", \"title\": \"在热气球节上迎接第一缕阳光\"}";
        LineIterator lineIterator = new LineIterator(new StringReader(msg1));
        ArrayList<LineIterator> lineIterators = new ArrayList<>();
        lineIterators.add(lineIterator);
        fileProducer.produceFromFile(lineIterators);
    }
}