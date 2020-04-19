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
public class ServerConfig {
    private static final String SERVERS_FILES = "server.properties";
    private static final String TAREGT_SERVER_USER = "target.server.user";
    private static final String TAREGT_SERVER_HOST = "target.server.host";
    private static final String TAREGT_SERVER_PORT = "target.server.port";
    private static final String TAREGT_SERVER_KEYFILE = "target.server.keyfile";

    protected ApplicationOptions applicationOptions;

    @Autowired
    public ServerConfig (ApplicationOptions applicationOptions) {
        this.applicationOptions = applicationOptions;
        this.loadConfig(SERVERS_FILES);
    }

    //server config
    private String targetUser;
    private int targetPort;
    private String targetHost;
    private String targetKeyfile;

    //file config
    private String targerfile;
    private String targetdir;
    private String processedfile;

    public String getTargetUser() {
        return targetUser;
    }

    public void setTargetUser(String targetUser) {
        this.targetUser = targetUser;
    }

    public int getTargetPort() {
        return targetPort;
    }

    public void setTargetPort(int targetPort) {
        this.targetPort = targetPort;
    }

    public String getTargetHost() {
        return targetHost;
    }

    public void setTargetHost(String targetHost) {
        this.targetHost = targetHost;
    }

    public String getTargetKeyfile() {
        return targetKeyfile;
    }

    public void setTargetKeyfile(String targetKeyfile) {
        this.targetKeyfile = targetKeyfile;
    }

    public String getTargerfile() {
        return targerfile;
    }

    public void setTargerfile(String targerfile) {
        this.targerfile = targerfile;
    }

    public String getTargetdir() {
        return targetdir;
    }

    public void setTargetdir(String targetdir) {
        this.targetdir = targetdir;
    }

    public String getProcessedfile() {
        return processedfile;
    }

    public void setProcessedfile(String processedfile) {
        this.processedfile = processedfile;
    }

    /**
     * using properties set the server config
     * @param configFile
     */
    public void loadConfig (String configFile){
        try {
            applicationOptions.init(configFile);
        } catch (IOException e) {
            log.error("Failed to read properties file. " + e);
        }
        this.setTargetUser(applicationOptions.getByNameString(TAREGT_SERVER_USER));
        this.setTargetHost(applicationOptions.getByNameString(TAREGT_SERVER_HOST));
        this.setTargetPort(Integer.parseInt(applicationOptions.getByNameString(TAREGT_SERVER_PORT)));
        this.setTargetKeyfile(applicationOptions.getByNameString(TAREGT_SERVER_KEYFILE));
    }
}
