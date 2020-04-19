package com.tongji.mind.service;

import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.SftpException;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;


@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
public class TrainModelTest {

    @Autowired
    private TrainModel trainModel;

    @Test
    public void testFileIsExisted() throws FileNotFoundException, JSchException, SftpException {
        List<String> uploadModelNames = new ArrayList<>();
        uploadModelNames.add("testUploadFile");
        Assert.assertTrue(trainModel.isFileExisted(uploadModelNames));
    }

}