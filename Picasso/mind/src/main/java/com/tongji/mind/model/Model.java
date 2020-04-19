package com.tongji.mind.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;

/**
 * @author: guangxush
 * @create: 2020/04/19
 */
@Entity
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "model")
public class Model {
    /**
     * 自增id
     */
    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * 模型名称
     */
    @Column(name = "name")
    private String name;

    /**
     * 实验结果：json格式数据
     */
    @Column(name = "result")
    private String result;

    /**
     * 模型结果，top K
     */
    @Column(name = "top")
    private Long top;
}
