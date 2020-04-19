package com.tongji.mind.controller;

import com.alibaba.fastjson.JSONObject;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.tongji.mind.model.Model;
import com.tongji.mind.service.ModelService;
import junit.framework.TestCase;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.context.WebApplicationContext;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
public class ModelControllerTest extends TestCase {

    @Autowired
    private WebApplicationContext wac;

    @Autowired
    private ModelService modelService;

    @Autowired
    private ObjectMapper mapper;

    private MockMvc mockMvc;

    @Before
    public void setup() {
        this.mockMvc = MockMvcBuilders.webAppContextSetup(this.wac).build();
    }

    @Test
    @Transactional
    public void testUpdate() throws Exception {
        Model model = Model.builder().name("cnn").build();
        Assert.assertNotNull(modelService.save(model));
        Map<String, Object> map = new HashMap<>();
        map.put("name", "cnn");
        String json = JSONObject.toJSONString(map);
        MvcResult result = mockMvc.perform(post("/insert")
                .contentType(MediaType.APPLICATION_JSON_UTF8).content(json)
                .accept(MediaType.APPLICATION_JSON_UTF8))
                .andDo(print())
                .andExpect(status().isOk())
                .andReturn();
        String response = result.getResponse().getContentAsString();
        System.out.println(response);
        Assert.assertTrue(response.contains("success"));
        map.put("result", "{\"f1\":0.97}");
        map.put("top", 1L);
        json = JSONObject.toJSONString(map);
        result = mockMvc.perform(post("/update")
                .contentType(MediaType.APPLICATION_JSON_UTF8).content(json)
                .accept(MediaType.APPLICATION_JSON_UTF8))
                .andDo(print())
                .andExpect(status().isOk())
                .andReturn();
        response = result.getResponse().getContentAsString();
        System.out.println(response);
        Assert.assertTrue(response.contains("success"));
    }

    @Test
    @Transactional
    public void testQuery() throws Exception{
        Model model = Model.builder().name("cnn").build();
        Assert.assertNotNull(modelService.save(model));
        String result = mockMvc.perform(get("/query")
                .param("name", "cnn")
                .contentType(MediaType.APPLICATION_JSON_UTF8))
                .andDo(print())
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();
        System.out.println(result);
    }

    @Test
    public void testUploadFile()throws Exception{
        List<String> list = new ArrayList<>();
        list.add("testUploadFile");
        String json = JSONObject.toJSONString(list);
        MvcResult result = mockMvc.perform(post("/upload")
                .contentType(MediaType.APPLICATION_JSON_UTF8).content(json)
                .accept(MediaType.APPLICATION_JSON_UTF8))
                .andDo(print())
                .andExpect(status().isOk())
                .andReturn();
        String response = result.getResponse().getContentAsString();
        System.out.println(response);
        Assert.assertTrue(response.contains("success"));
    }
}