package com.tongji.user.service.impl;

import com.tongji.user.model.User;
import com.tongji.user.model.UserVO;
import com.tongji.user.service.UserService;
import junit.framework.TestCase;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.transaction.annotation.Transactional;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
public class UserServiceImplTest extends TestCase {

    @Autowired
    UserService userService;

    @Test
    @Transactional
    public void testLogin() {
        User user = User.builder().uid("123456").userInfo("hello").build();
        userService.register(user);
        Assert.assertTrue(userService.login("123456"));
    }

    @Test
    @Transactional
    public void testRegister() {
        User user = User.builder().uid("1234579").userInfo("hello").build();
        UserVO userVO = UserVO.builder().uid("1234579").userInfo("hello").build();
        Assert.assertEquals(userService.register(user), userVO);
    }

    @Test
    @Transactional
    public void testUpdate() {
        User userOld = User.builder().uid("123457").userInfo("hello").build();
        User userNew = User.builder().uid("123457").userInfo("hello hello").build();
        UserVO userVO = UserVO.builder().uid("123457").userInfo("hello hello").build();
        Assert.assertEquals(userService.update(userNew), userVO);
        Assert.assertNotEquals(userOld, userVO);
    }
}