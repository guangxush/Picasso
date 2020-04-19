package com.tongji.mind.util;

import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Component;

/**
 * @author: guangxush
 * @create: 2020/04/19
 */
@Component
@Slf4j
public class SSHWrapper {

    private static final String STRICT_HOST_KEY_CHECKING_KEY = "StrictHostKeyChecking";
    private static final String STRICT_HOST_KEY_CHECKING_VALUE = "no";
    private static final String CHANNEL_TYPE = "sftp";

    @Value("${config.target.keyfile}")
    private String keyfile;

    @Value("${config.target.user}")
    private String user;

    @Value("${config.target.host}")
    private String host;

    @Value("${config.target.port}")
    private int port;

    @Value("${config.target.password}")
    private String password;

    /**
     * ssh to server
     * */
    @Retryable(value = JSchException.class,maxAttempts = 5, backoff = @Backoff(delay = 60000))
    public ChannelSftp connect() throws JSchException {
        JSch jsch = new JSch();
        jsch.addIdentity(keyfile);
        JSch.setConfig(STRICT_HOST_KEY_CHECKING_KEY, STRICT_HOST_KEY_CHECKING_VALUE);

        // ssh connection from site to target server
        Session targetSession = jsch.getSession(user, host, port);
        targetSession.setHostKeyAlias(host);
        targetSession.setPassword(password);
        targetSession.connect();
        log.info("Connected to " + user + "@" + host + ":" + port);

        ChannelSftp channel = (ChannelSftp) targetSession.openChannel(CHANNEL_TYPE);
        channel.connect();
        return channel;
    }
}
