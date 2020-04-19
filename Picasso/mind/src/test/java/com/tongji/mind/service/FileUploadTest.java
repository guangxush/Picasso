package com.tongji.mind.service;

import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.SftpException;
import com.tongji.mind.util.SSHWrapper;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;

import static org.junit.Assert.*;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
public class FileUploadTest {

    @Autowired
    private FileUpload fileUpload;

    @Value("${config.file.sources}")
    private String sourcesDir;

    @Test
    public void configValue(){
        Assert.assertEquals(sourcesDir, "../../News_Classification/classification/");
    }

    @Test
    public void testUploadFile() throws FileNotFoundException, SftpException, JSchException {
        List<String> uploadModelNames = new ArrayList<>();
        uploadModelNames.add("testUploadFile");
        Assert.assertTrue(fileUpload.uploadFile(uploadModelNames));
    }
}