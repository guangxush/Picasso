package com.tongji.user.controller;

import com.alibaba.fastjson.JSONObject;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.tongji.user.model.User;
import com.tongji.user.service.UserService;
import junit.framework.TestCase;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.context.WebApplicationContext;

import java.util.HashMap;
import java.util.Map;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
public class UserControllerTest extends TestCase {

    private static final String APP_HEADER = "tongji";

    private MockMvc mockMvc;

    @Autowired
    UserService userService;

    @Autowired
    private WebApplicationContext wac;

    @Autowired
    private ObjectMapper mapper;

    @Before
    public void setup() {
        this.mockMvc = MockMvcBuilders.webAppContextSetup(this.wac).build();
    }

    @Test
    @Transactional
    public void testLogin() throws Exception {
        User user = User.builder().uid("123456").userInfo("hello").build();
        userService.register(user);
        Assert.assertTrue(userService.login("123456"));
        Map<String, Object> map = new HashMap<>();
        map.put("uid", "123456");
        String json = JSONObject.toJSONString(map);
        MvcResult result = mockMvc.perform(post("/login")
                .contentType(MediaType.APPLICATION_JSON_UTF8).content(json)
                .header("app_head", "tongji")
                .accept(MediaType.APPLICATION_JSON_UTF8))
                .andDo(print())
                .andExpect(status().isOk())
                .andReturn();
        String response = result.getResponse().getContentAsString();
        System.out.println(response);
        Assert.assertTrue(response.contains("success"));
    }

    @Test
    @Transactional
    public void testRegister() throws Exception {
        Map<String, Object> map = new HashMap<>();
        map.put("uid", "1234510");
        map.put("userInfo", "hello");
        String json = JSONObject.toJSONString(map);
        MvcResult result = mockMvc.perform(post("/register")
                .contentType(MediaType.APPLICATION_JSON_UTF8).content(json)
                .header("app_head", "tongji")
                .accept(MediaType.APPLICATION_JSON_UTF8))
                .andDo(print())
                .andExpect(status().isOk())
                .andReturn();
        String response = result.getResponse().getContentAsString();
        System.out.println(response);
        Assert.assertTrue(response.contains("success"));
    }

    @Test
    @Transactional
    public void testUpdate() throws Exception {
        Map<String, Object> map = new HashMap<>();
        map.put("uid", "123459");
        map.put("userInfo", "hello2");
        String json = JSONObject.toJSONString(map);
        MvcResult result = mockMvc.perform(post("/update")
                .contentType(MediaType.APPLICATION_JSON_UTF8).content(json)
                .header("app_head", "tongji")
                .accept(MediaType.APPLICATION_JSON_UTF8))
                .andDo(print())
                .andExpect(status().isOk())
                .andReturn();
        String response = result.getResponse().getContentAsString();
        System.out.println(response);
        Assert.assertTrue(response.contains("success"));
    }
}