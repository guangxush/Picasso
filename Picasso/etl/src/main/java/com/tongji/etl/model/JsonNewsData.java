package com.tongji.etl.model;

import lombok.Builder;
import lombok.Data;

/**
 * @author: guangxush
 * @create: 2020/04/17
 */
@Data
@Builder
public class JsonNewsData {

    private Long id;
    private String title;
    private String label;

}
