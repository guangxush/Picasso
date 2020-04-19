package com.tongji.mind.service;

import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.SftpException;
import com.tongji.mind.util.SSHWrapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.List;

/**
 * @author: guangxush
 * @create: 2020/04/19
 */
@Service
@Slf4j
public class TrainModel {

    @Value("${config.file.target}")
    private String targetDir;

    @Autowired
    private SSHWrapper sshWrapper;

    /**
     * todo
     * train the model file on server
     * @param modelName
     * @return
     * @throws FileNotFoundException
     * @throws JSchException
     * @throws SftpException
     */
    public boolean trainModel(List<String> modelName) throws FileNotFoundException, JSchException, SftpException {
        if(isFileExisted(modelName)){
            // rpc or post to server
        }
        return false;
    }

    /**
     * check the model file existed
     *
     * @param uploadModelNames
     * @return
     * @throws JSchException
     * @throws SftpException
     * @throws FileNotFoundException
     */
    public boolean isFileExisted(List<String> uploadModelNames) throws JSchException, SftpException, FileNotFoundException {
        ChannelSftp channel = sshWrapper.connect();
        try {
            if (targetDir != null && !"".equals(targetDir)) {
                channel.cd(targetDir);
            } else {
                return false;
            }
            boolean fileExisted = true;
            for (String uploadFileName : uploadModelNames) {
                if (channel.get(uploadFileName + ".py") == null) {
                    fileExisted = false;
                }
            }
            return fileExisted;
        } catch (SftpException e) {
            log.error("Errors happened in SftpException: " + e.getMessage());
            throw new SftpException(e.id, e.getMessage());
        } finally {
            channel.exit();
        }
    }
}
