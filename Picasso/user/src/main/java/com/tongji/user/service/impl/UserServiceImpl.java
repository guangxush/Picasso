package com.tongji.user.service.impl;

import com.tongji.common.exception.AppInternalError;
import com.tongji.user.model.User;
import com.tongji.user.model.UserVO;
import com.tongji.user.repository.UserRepo;
import com.tongji.user.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

/**
 * @author: guangxush
 * @create: 2020/04/13
 */
@Service
@Slf4j
public class UserServiceImpl implements UserService {

    @Autowired
    private UserRepo userRepo;

    @Override
    public Boolean login(String uid) {
        Optional<User> user = userRepo.findUserByUid(uid);
        if (user.isPresent()) {
            return true;
        }
        return false;
    }

    @Override
    public UserVO register(User user) {
        UserVO userVO;
        String userUid = user.getUid();
        if (userUid == null) {
            log.error("user id is null");
            throw new AppInternalError("user id is null, user info:{}", user.toString());
        }
        Optional<User> userInDb = userRepo.findUserByUid(user.getUid());
        try {
            if (userInDb.isPresent()) {
                //更新操作
                if (userUid.equals(userInDb.get().getUid())) {
                    //账号已经注册过
                    log.error("This userid has been used!");
                    return null;
                }
            }
            //插入操作
            userVO = saveUser(user);
        } catch (Exception e) {
            return null;
        }
        return userVO;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public UserVO update(User user) {
        UserVO userVO;
        String userUid = user.getUid();
        if (userUid == null) {
            log.error("user id is null");
            throw new AppInternalError("user id is null, user info:{}", user.toString());
        }
        Optional<User> userInDb = userRepo.findUserByUid(user.getUid());
        try {
            if (userInDb.isPresent()) {
                if (!userUid.equals(userInDb.get().getUid())) {
                    //账号未注册过
                    log.error("This userid has not been registered!");
                    throw new AppInternalError("This userid {} has been registered!", user.getUid());
                }
            }
            //更新操作
            user.setId(userInDb.get().getId());
            userVO = saveUser(user);
        } catch (Exception e) {
            return null;
        }
        return userVO;
    }

    /**
     * 保存用户信息
     *
     * @param user
     * @return
     */
    private UserVO saveUser(User user) {
        user = userRepo.save(user);
        if (user.getId() <= 0) {
            log.error("fail to save the user:{}", user.toString());
            throw new AppInternalError("fail to save the user:{}", user.toString());
        }
        return UserVO.builder().uid(user.getUid()).userInfo(user.getUserInfo()).build();
    }
}
