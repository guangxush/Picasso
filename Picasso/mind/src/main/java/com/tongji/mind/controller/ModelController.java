package com.tongji.mind.controller;

import com.tongji.common.model.ApiResponse;
import com.tongji.mind.model.Model;
import com.tongji.mind.service.ModelService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import static com.tongji.common.constant.HeadConstant.APP_HEAD;

/**
 * @author: guangxush
 * @create: 2020/04/19
 */

@RestController
@Slf4j
public class ModelController {

    @Autowired
    ModelService modelService;

    /**
     * 模型信息更新
     *
     * @param model
     * @return
     */
    @RequestMapping(path = {"update", "insert"}, method = RequestMethod.POST)
    @ResponseBody
    public ApiResponse<Model> update(@RequestBody Model model) {
        Model savedModel = modelService.save(model);
        if (savedModel != null) {
            return new ApiResponse<Model>().success(savedModel);
        } else {
            return new ApiResponse<Model>().fail(null);
        }
    }

    /**
     * 模型结果查询
     *
     * @param name
     * @return
     */
    @RequestMapping(path = "/query", method = RequestMethod.GET)
    @ResponseBody
    public ApiResponse<Model> query(@RequestParam String name) {
        Model model = modelService.query(name);
        if (model != null) {
            return new ApiResponse<Model>().success(model);
        } else {
            return new ApiResponse<Model>().fail(null);
        }
    }

}
