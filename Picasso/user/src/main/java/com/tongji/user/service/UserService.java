package com.tongji.user.service;

import com.tongji.user.model.User;
import com.tongji.user.model.UserVO;

/**
 * @author: guangxush
 * @create: 2020/04/13
 */
public interface UserService {
    /**
     * 用户登录
     * @param uid
     * @return
     */
    Boolean login(String uid);

    /**
     * 用户注册
     * @param user
     * @return
     */
    UserVO register(User user);

    /**
     * 用户信息保存
     * @param user
     * @return
     */
    UserVO update(User user);
}
