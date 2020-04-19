package com.tongji.etl.util;

import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;
import com.tongji.etl.model.ServerConfig;
import lombok.extern.slf4j.Slf4j;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Component;

/**
 * @author: guangxush
 * @create: 2020/04/17
 */
@Component
@Slf4j
public class SSHWrapper {

    private static final String STRICT_HOST_KEY_CHECKING_KEY = "StrictHostKeyChecking";
    private static final String STRICT_HOST_KEY_CHECKING_VALUE = "no";
    private static final String CHANNEL_TYPE = "sftp";

    /**
     * ssh to server
     * @param serverConfig
     * */
    @Retryable(value = JSchException.class,maxAttempts = 5, backoff = @Backoff(delay = 60000))
    public ChannelSftp connect(ServerConfig serverConfig) throws JSchException {
        String targetKeyFile = serverConfig.getTargetKeyfile();
        String targetUser = serverConfig.getTargetUser();
        String targetHost = serverConfig.getTargetHost();
        int targetPort = serverConfig.getTargetPort();

        JSch jsch = new JSch();
        jsch.addIdentity(targetKeyFile);
        JSch.setConfig(STRICT_HOST_KEY_CHECKING_KEY, STRICT_HOST_KEY_CHECKING_VALUE);

        // ssh connection from site to target server
        Session targetSession = jsch.getSession(targetUser, targetHost, targetPort);
        targetSession.setHostKeyAlias(targetHost);
        targetSession.setPassword("shgx");
        targetSession.connect();
        log.info("Connected to " + targetUser + "@" + targetHost + ":" + targetPort);

        ChannelSftp channel = (ChannelSftp) targetSession.openChannel(CHANNEL_TYPE);
        channel.connect();
        return channel;
    }
}
