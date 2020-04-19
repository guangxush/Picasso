package com.tongji.etl.service;

import junit.framework.TestCase;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
public class ScheduledTaskTest extends TestCase {

    @Autowired
    ScheduledTask scheduledTask;

    @Test
    public void testTestRun() {
        scheduledTask.run();
    }
}