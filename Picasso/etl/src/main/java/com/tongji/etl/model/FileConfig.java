package com.tongji.etl.model;

import com.tongji.etl.util.ApplicationOptions;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.IOException;

/**
 * @author: guangxush
 * @create: 2020/04/17
 */
@Component
@Slf4j
public class FileConfig extends ServerConfig{

    private static final String SERVERS_FILES = "server.properties";
    private static final String FILE_TARGETDIR = "file.targetdir";
    private static final String FILE_TARGETFILE = "file.targetfile";
    private static final String FILE_PROCESSEDFILE = "file.processedfile";

    @Autowired
    public FileConfig (ApplicationOptions applicationOptions) {
        super(applicationOptions);
        this.applicationOptions = applicationOptions;
        this.loadConfig(SERVERS_FILES);
    }

    /**
     * using properties set the file in server
     * @param configFile
     */
    @Override
    public void loadConfig (String configFile){
        try {
            applicationOptions.init(configFile);
        } catch (IOException e) {
            log.error("Failed to read properties file. " + e);
        }
        this.setTargetdir(applicationOptions.getByNameString(FILE_TARGETDIR));
        this.setTargerfile(applicationOptions.getByNameString(FILE_TARGETFILE));
        this.setProcessedfile(applicationOptions.getByNameString(FILE_PROCESSEDFILE));
    }
}
