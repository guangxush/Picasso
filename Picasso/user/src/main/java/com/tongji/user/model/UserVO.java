package com.tongji.user.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @author: guangxush
 * @create: 2020/04/13
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserVO {
    /**
     * 账号
     */
    private String uid;

    /**
     * 用户信息
     */
    private String userInfo;
}
