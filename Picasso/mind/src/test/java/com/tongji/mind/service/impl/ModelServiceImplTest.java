package com.tongji.mind.service.impl;

import com.tongji.mind.model.Model;
import com.tongji.mind.service.ModelService;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.transaction.annotation.Transactional;


@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
public class ModelServiceImplTest {

    @Autowired
    private ModelService modelService;

    @Test
    @Transactional
    public void save() {
        Model model = Model.builder().name("cnn").build();
        Assert.assertNotNull(modelService.save(model));
        model.setResult("{\"f1\":0.97}");
        model.setTop(1L);
        Assert.assertEquals(modelService.save(model), model);
        System.out.println(modelService.save(model));
    }

    @Test
    @Transactional
    public void query() {
        Model model = Model.builder().name("cnn").build();
        Assert.assertNotNull(modelService.save(model));
        Assert.assertEquals(model, modelService.query("cnn"));
        System.out.println(modelService.query("cnn"));
    }
}