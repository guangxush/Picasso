package com.tongji.mind.service;

import com.tongji.mind.model.Model;

/**
 * @author: guangxush
 * @create: 2020/04/19
 */
public interface ModelService {

    /**
     * 保存模型训练结果
     * @param model
     * @return
     */
    Model save(Model model);


    /**
     * 根据name查询结果
     * @param name
     * @return
     */
    Model query(String name);

}
