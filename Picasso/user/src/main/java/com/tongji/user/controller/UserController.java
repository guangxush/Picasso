package com.tongji.user.controller;

import com.tongji.common.model.ApiResponse;
import com.tongji.user.model.User;
import com.tongji.user.model.UserVO;
import com.tongji.user.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import static com.tongji.common.constant.HeadConstant.APP_HEAD;

/**
 * @author: guangxush
 * @create: 2020/04/13
 */
@RestController
@Slf4j
public class UserController {

    @Autowired
    UserService userService;

    @Value("${app.header}")
    private String header;

    /**
     * 用户登录
     * @param sHead
     * @param user
     * @return
     */
    @RequestMapping(path = "/login", method = RequestMethod.POST)
    @ResponseBody
    public ApiResponse<Boolean> login(@RequestHeader(APP_HEAD) String sHead,
                                      @RequestBody User user){
        if(!sHead.equals(header)){
            return new ApiResponse<Boolean>().fail(false);
        }
        Boolean result = userService.login(user.getUid());
        if(result){
            return new ApiResponse<Boolean>().success(true);
        } else{
            return new ApiResponse<Boolean>().fail(false);
        }
    }

    /**
     * 用户注册
     * @param sHead
     * @param user
     * @return
     */
    @RequestMapping(path = "/register", method = RequestMethod.POST)
    @ResponseBody
    public ApiResponse<UserVO> register(@RequestHeader(APP_HEAD) String sHead,
                                        @RequestBody User user){
        if(!sHead.equals(header)){
            return new ApiResponse<UserVO>().fail(null);
        }
        UserVO userVO = userService.register(user);
        if(userVO!=null){
            return new ApiResponse<UserVO>().success(userVO);
        } else{
            return new ApiResponse<UserVO>().fail(userVO);
        }
    }

    /**
     * 用户更新信息
     * @param sHead
     * @param user
     * @return
     */
    @RequestMapping(path = "/update", method = RequestMethod.POST)
    @ResponseBody
    public ApiResponse<UserVO> update(@RequestHeader(APP_HEAD) String sHead,
                                        @RequestBody User user){
        if(!sHead.equals(header)){
            return new ApiResponse<UserVO>().fail(null);
        }
        UserVO userVO = userService.update(user);
        if(userVO!=null){
            return new ApiResponse<UserVO>().success(userVO);
        } else{
            return new ApiResponse<UserVO>().fail(userVO);
        }
    }
}
