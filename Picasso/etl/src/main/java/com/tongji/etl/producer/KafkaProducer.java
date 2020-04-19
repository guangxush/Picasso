package com.tongji.etl.producer;

import com.tongji.etl.model.JsonNewsData;
import org.apache.commons.io.LineIterator;

import java.util.ArrayList;

/**
 * @author: guangxush
 * @create: 2020/04/17
 */
public abstract class KafkaProducer {
    /**
     * produce the data from file
     * @param fileLineIterators
     */
    public abstract void produceFromFile (ArrayList<LineIterator> fileLineIterators);

    /**
     * produce the data from web services
     * @param jsonNewsDataArray
     */
    public abstract void produceFromService (JsonNewsData[] jsonNewsDataArray);
}
