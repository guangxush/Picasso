package com.tongji.user.service.impl;

import com.google.common.cache.CacheBuilder;
import com.google.common.cache.CacheLoader;
import com.google.common.cache.CacheStats;
import com.google.common.cache.LoadingCache;
import com.tongji.common.exception.AppInternalError;
import com.tongji.user.model.User;
import com.tongji.user.model.UserVO;
import com.tongji.user.repository.UserRepo;
import com.tongji.user.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.PostConstruct;
import java.util.Optional;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;

/**
 * @author: guangxush
 * @create: 2020/04/13
 */
@Service
@Slf4j
public class UserServiceImpl implements UserService {

    @Autowired
    private UserRepo userRepo;

    private static Long cacheSize = 2000L;
    private static Long expireDays = 10L;

    @PostConstruct
    public void init() {
        // unused
        cacheSize = 2000L;
        expireDays = 10L;
    }

    private LoadingCache<String, User> userCache = CacheBuilder.newBuilder()
            .recordStats()
            .maximumSize(cacheSize)
            .expireAfterAccess(expireDays, TimeUnit.DAYS)
            .build(
                    new CacheLoader<String, User>() {
                        @Override
                        public User load(String uid) throws Exception {
                            User user = queryFromDB(uid);
                            if (user != null) {
                                return user;
                            }
                            return User.builder().uid("unknown").userInfo("unknown").build();
                        }
                    }
            );

    @Override
    public Boolean login(String uid) {
        Optional<User> user = userRepo.findUserByUid(uid);
        if (user.isPresent()) {
            return true;
        }
        return false;
    }

    private User queryFromDB(String uid) {
        Optional<User> user = userRepo.findUserByUid(uid);
        return user.orElse(null);
    }

    @Override
    public User queryByCache(String uid) {
        if (uid == null || uid.equals("")) {
            log.error("the ids is null");
            throw new NullPointerException("the ids is null");
        }
        User user = null;
        //从缓存中取
        try {
            User userFromCache = userCache.get(uid);
            if (userFromCache != null) {
                user = userFromCache;
            }
            return user;
        } catch (ExecutionException e) {
            log.error("take books from guava cache error, ids : {}", uid, e);
        }
        //从DB中取
        user = queryFromDB(uid);
        return user;
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

    /**
     * 将缓存状态定时记录在日志中
     *
     * @param
     * @return
     */
    @Scheduled(fixedRate = 1000 * 60 * 5)
    private void recordCacheStatus() {
        CacheStats stats = userCache.stats();
        log.info("guava cache status : {}", stats.toString());
    }
}
