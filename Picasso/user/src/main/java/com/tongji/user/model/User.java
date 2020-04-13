package com.tongji.user.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;

/**
 * @author: guangxush
 * @create: 2020/04/13
 */
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "user")
public class User {
    /**
     * 用户表自增id
     */
    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * 账号
     */
    @Column(name = "uid")
    private String uid;

    /**
     * 用户信息
     */
    @Column(name = "userinfo")
    private String userInfo;
}
