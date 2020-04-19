package com.tongji.etl.service;

import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.SftpException;
import com.tongji.etl.model.FileConfig;
import com.tongji.etl.model.ServerConfig;
import com.tongji.etl.producer.FileProducer;
import com.tongji.etl.repository.ProcessRepo;
import com.tongji.etl.util.MailSend;
import com.tongji.etl.util.SSHWrapper;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.LineIterator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

/**
 * @author: guangxush
 * @create: 2020/04/17
 */
@Service
@Configuration
@Slf4j
public class ScheduledTask {
    private ChannelSftp channel;

    @Autowired
    //@Qualifier("ServerConfig")
    private ServerConfig serverConfig;

    @Autowired
    private FileConfig fileConfig;

    @Autowired
    private ProcessRepo processRepo;

    @Autowired
    private SSHWrapper sshWrapper;

    @Autowired
    private FileWatcher fileWatcher;

    @Autowired
    private FileProducer fileProducer;

    @Autowired
    private MailSend mailSend;

    public void run() {
        try {
            //send news data to kafka
            channel = sshWrapper.connect(serverConfig);
            fileWatcher = new FileWatcher(fileConfig, processRepo);
            ArrayList<LineIterator> fileLineIterators = fileWatcher.getFileIterator(channel);
            if (fileLineIterators != null && fileLineIterators.size() > 0) {
                fileProducer.produceFromFile(fileLineIterators);
            }
            if (fileWatcher.updateProcessStatus(channel)) {
                System.out.println("news data sent successfully to kafka!");
                //mailSend.sendmail("news data sent successfully to kafka!");
            }
        } catch (IOException ioe) {
            log.error("IOException happened", ioe);
        } catch (SftpException sftpe) {
            log.error("SftpException happened", sftpe);
        } catch (JSchException jsche) {
            log.error("JSchException happened", jsche);
        } finally {
            channel.exit();
        }
    }

    /**
     * scheduled task at 12 AM
     * */
    @Scheduled(cron = "0 0 12 * * ?")
    public void scheduleTask(){
        log.info("Scheduled on " + new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date()));
        run();
    }
}
