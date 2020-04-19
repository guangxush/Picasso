package com.tongji.etl.util;

import junit.framework.TestCase;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@SpringBootTest
@RunWith(SpringJUnit4ClassRunner.class)
public class MailSendTest {

    @Autowired
    private MailSend mailSend;

    @Test
    public void testSendEmail () {
        mailSend.sendmail("666");
    }
}