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
public class FileUpload {

    private final String NO_SUCH_FILE = "No such file";

    @Value("${config.file.sources}")
    private String sourcesDir;

    @Value("${config.file.target}")
    private String targetDir;

    @Autowired
    private SSHWrapper sshWrapper;

    /**
     * upload the file into server
     *
     * @param uploadModelNames
     * @return
     * @throws SftpException
     * @throws FileNotFoundException
     */

    public boolean uploadFile(List<String> uploadModelNames) throws JSchException, SftpException, FileNotFoundException {
        ChannelSftp channel = sshWrapper.connect();
        try {
            for (String uploadFileName : uploadModelNames) {
                String uploadFile = sourcesDir + uploadFileName + ".py";
                String targetFile = targetDir + uploadFileName + ".py";
                channel.put(new FileInputStream(uploadFile), targetFile);
            }
            return true;
        } catch (SftpException e) {
            log.error("Errors happened in SftpException: " + e.getMessage());
            throw new SftpException(e.id, e.getMessage());
        } catch (FileNotFoundException e) {
            log.error("Errors happened in FileNotFoundException: " + e.getMessage());
            throw new FileNotFoundException(e.getMessage());
        }
        finally {
            channel.exit();
        }
    }
}
