package com.tongji.mind.service.impl;

import com.tongji.common.exception.AppInternalError;
import com.tongji.mind.model.Model;
import com.tongji.mind.repository.ModelRepo;
import com.tongji.mind.service.ModelService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

/**
 * @author: guangxush
 * @create: 2020/04/19
 */
@Service
@Slf4j
public class ModelServiceImpl implements ModelService {

    @Autowired
    private ModelRepo modelRepo;

    @Override
    public Model save(Model model) {
        if(model==null || model.getName()==null){
            log.error("model or model name isn't null");
            throw new AppInternalError("model or model name isn't null");
        }
        Optional<Model> modelInDb = modelRepo.findByName(model.getName());
        if(modelInDb.isPresent()){
            Model oldModel = modelInDb.get();
            model.setId(oldModel.getId());
        }
        return saveModel(model);
    }

    @Override
    public Model query(String name) {
        Optional<Model> model = modelRepo.findByName(name);
        return model.get();
    }

    /**
     * 保存模型信息
     *
     * @param model
     * @return
     */
    private Model saveModel(Model model) {
        model = modelRepo.save(model);
        if (model.getId() <= 0) {
            log.error("fail to save the model:{}", model.toString());
            throw new AppInternalError("fail to save the user:{}", model.toString());
        }
        return model;
    }
}
