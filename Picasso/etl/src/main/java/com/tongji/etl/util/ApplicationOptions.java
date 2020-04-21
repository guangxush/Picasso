package com.tongji.etl.util;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;
import java.util.ServiceConfigurationError;

/**
 * @author: guangxush
 * @create: 2020/04/17
 */
@Component
@Scope("prototype")
public class ApplicationOptions {

    private Properties properties;

    /**
     * init the properties file
     * @param inputFile
     * @throws IOException
     */
    public void init(String inputFile) throws IOException {
        // InputStream in = this.getClass().getResourceAsStream("/"+inputFile);
        File file = new File("etl/src/main/resources/config/"+inputFile);
        //File file = new File("src/main/resources/config/"+inputFile); //仅测试时使用
        Properties props = new Properties();
        FileInputStream fileInputStream = new FileInputStream(file);
        props.load(fileInputStream);
        this.properties = props;
    }

    /**
     * get the param from properties
     * @param key
     * @return
     */
    public String getByNameString (String key) {
        if (!properties.containsKey(key)) {
            throw new ServiceConfigurationError("Configuration property not found: " + key);
        }
        return properties.getProperty(key);
    }

}
