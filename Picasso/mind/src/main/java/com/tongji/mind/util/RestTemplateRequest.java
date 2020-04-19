package com.tongji.mind.util;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.tongji.common.model.ApiResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Objects;

/**
 * @author: guangxush
 * @create: 2020/04/19
 */
@Slf4j
@Service
public class RestTemplateRequest {

    @Autowired
    private RestTemplateBuilder builder;

    private ObjectMapper om = new ObjectMapper();

    public Boolean jsonRequest(String url, Object object) {
        Boolean sendResult = false;
        RestTemplate restTemplate = builder.build();
        String objectJson = "";
        try {
            objectJson = new ObjectMapper().writeValueAsString(object);
        } catch (Exception e) {
            log.error("can't trans the {} object to json string!", object);
        }
        String request = url;
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<String> requestEntity = new HttpEntity<>(objectJson, headers);
        try {
            ResponseEntity<String> entity = restTemplate.postForEntity(request, requestEntity, String.class);
            //如果请求数据成功，获取请求之后的值
            if (entity.getStatusCode() == HttpStatus.OK) {
                JsonNode jsonNode = new ObjectMapper().readTree(entity.getBody());
                sendResult = Boolean.valueOf(jsonNode.get("data").asText());
                if (!sendResult) {
                    log.info("send {} failed!, the return result is {}.", object, sendResult);
                }
                log.info("send {} succeed!", object);
            } else {
                log.error("send {}  failed, the status is {}!, the entity is {}, the url is {}!", object,
                        entity.getStatusCode(), requestEntity.toString(), url);
            }
        } catch (Exception e) {
            log.error("send {}  failed!", object);
            throw new InternalError(String.format("send %s  failed!, the error is %s", object, e));
        }
        return sendResult;
    }

    /**
     * 带参数的url请求
     *
     * @param url
     * @param args
     * @return
     */
    public Object paramRequest(String url, String... args) {
        Objects objects = null;
        RestTemplate restTemplate = builder.build();
        if (url == null) {
            log.error("the url is null!");
            return null;
        }
        String request = url + "?param1=" + args[0] + "&param2=" + args[1];
        try {
            ResponseEntity<ApiResponse> entity = restTemplate.getForEntity(request, ApiResponse.class);
            //如果请求数据成功，返回结果
            if (entity.getStatusCode() == HttpStatus.OK) {
                objects = om.convertValue(Objects.requireNonNull(entity.getBody()).getData(),
                        new TypeReference<Objects>() {
                        });
                log.info("successfully get the user statistics!");
                return objects;
            } else {
                log.info("fail get the user statistics!, the return code is {}", entity.getStatusCode());
                return objects;
            }
        } catch (Exception e) {
            log.error("send the request {} failed!", request);
        }
        return objects;
    }
}
