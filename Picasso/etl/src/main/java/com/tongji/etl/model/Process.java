package com.tongji.etl.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;

/**
 * @author: guangxush
 * @create: 2020/04/18
 */
@Entity
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "process")
public class Process {
    /**
     * 自增id
     */
    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * 日期，格式为20200418
     */
    @Column(name = "date")
    private String date;

    /**
     * 新闻信息是否处理，0未处理，1处理，默认0
     */
    @Column(name = "processed")
    private int processed;
}
