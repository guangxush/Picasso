package com.tongji.etl.service;


import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.SftpException;
import com.tongji.etl.model.Process;
import com.tongji.etl.model.JsonNewsData;
import com.tongji.etl.model.ServerConfig;
import com.tongji.etl.repository.ProcessRepo;
import com.alibaba.fastjson.JSONObject;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.IOUtils;
import org.apache.commons.io.LineIterator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.io.InputStream;
import java.sql.SQLDataException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * @author: guangxush
 * @create: 2020/04/17
 */
@Service
@Slf4j
public class FileWatcher {

    public ArrayList<String> datesToProcess = new ArrayList<>();

    private final ServerConfig serverConfig;

    private final ProcessRepo processRepo;

    @Autowired(required = false)
    public FileWatcher(ServerConfig serverConfig, ProcessRepo processRepo) {
        this.serverConfig = serverConfig;
        this.processRepo = processRepo;
    }

    /**
     * get LineIterators to lazy load data and avoid load all data into memory at once
     *
     * @return ArrayList<LineIterator>
     */
    public ArrayList<LineIterator> getFileIterator(ChannelSftp channel) throws SftpException, IOException {
        ArrayList<LineIterator> fileLineIterators = new ArrayList<>();
        String targetFile = serverConfig.getTargetdir() + serverConfig.getTargerfile();
        InputStream inputStream = null;
        try {
            getUnProcessedNews();
            for (String date : datesToProcess) {
                // /data/shgx/Picasso/News_Classification/classification/data/test_data_20200418.txt
                inputStream = channel.get(targetFile + "_" + date + ".txt");
                LineIterator lineIterator = IOUtils.lineIterator(inputStream, "UTF-8");
                fileLineIterators.add(lineIterator);
            }
        } catch (SftpException ex) {
            log.error("Errors happened in SftpException ex: " + ex.getMessage());
            throw new SftpException(ex.id, ex.getMessage());
        } catch (IOException e) {
            log.error("Errors happened in IOException e: " + e.getMessage());
            throw new IOException(e.getMessage());
        }
        return fileLineIterators;
    }


    /**
     * update target files to processed ones
     * processedFilePattern = news_data_yyyymmdd.done
     */
    @Transactional(rollbackFor = SQLDataException.class)
    public Boolean updateProcessStatus(ChannelSftp channel) throws SftpException {
        int datesCnt = datesToProcess.size();
        int updateCnt = 0;
        try {
            for (String date : datesToProcess) {
                String doneFile = serverConfig.getTargetdir() + serverConfig.getTargerfile() + "_" + date + ".txt";
                String processedFile = serverConfig.getTargetdir() + serverConfig.getProcessedfile() + "_" + date + ".txt";
                channel.rename(doneFile, processedFile);
                updateProcessedInDB(date);
                updateCnt++;
            }
            datesToProcess.clear();
        } catch (SftpException e) {
            log.error("Errors happened in SftpException: " + e.getMessage());
            throw new SftpException(e.id, e.getMessage());
        }
        return updateCnt > 0 && updateCnt == datesCnt;
    }

    /**
     * update the process status in DB
     * @param date
     */
    private void updateProcessedInDB(String date){
        Optional<Process> processOptional = processRepo.findProcessByDate(date);
        if(processOptional.isPresent()){
            Process process = processOptional.get();
            process.setProcessed(1);
            processRepo.save(process);
        }
    }

    /**
     * look for unprocessed files in the target server and parse dates to process
     */
    public void getUnProcessedNews() {
        datesToProcess.clear();
        List<Process> unProcessedRecord = new ArrayList<>();
        try {
            unProcessedRecord = processRepo.queryUnprocessedRecords();
        } catch (Exception e) {
            log.error("SQL query error: " + e.getMessage());
        }
        for (Process process : unProcessedRecord) {
            datesToProcess.add(process.getDate());
        }
    }

    /**
     * parse the data file and load data into SchemaData
     *
     * @param line
     * @return SchemaData
     * {"id": 74, "label": "113", "title": "在热气球节上迎接第一缕阳光"}
     */
    public JsonNewsData parseFile(String line) {
        JSONObject jsonObject = (JSONObject) JSONObject.parse(line);
        return JsonNewsData.builder()
                .id(jsonObject.getLong("id"))
                .label(jsonObject.getString("label"))
                .title(jsonObject.getString("title"))
                .build();
    }
}
