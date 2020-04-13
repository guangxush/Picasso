package com.tongji.common.model;

import com.tongji.common.enums.APICodeEnum;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @author: guangxush
 * @create: 2020/04/13
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class ApiResponse<T> {
    @JsonFormat(shape = JsonFormat.Shape.STRING)
    APICodeEnum code;

    T data;

    @JsonProperty("message")
    String message;

    /**
     * 成功
     *
     * @param data
     * @return
     */
    public ApiResponse<T> success(T data) {
        this.code = APICodeEnum.SUCCESS;
        this.data = data;
        this.message = "success";
        return this;
    }

    /**
     * 失败
     *
     * @param message
     * @return
     */
    public ApiResponse<T> fail(T message) {
        this.code = APICodeEnum.FAILURE;
        this.data = message;
        this.message = "failure";
        return this;
    }

    /**
     * 未找到资源
     *
     * @param message
     * @return
     */
    public ApiResponse<T> notFound(T message) {
        this.code = APICodeEnum.NOT_FOUND;
        this.data = message;
        this.message = "not found";
        return this;
    }

    /**
     * 未授权
     *
     * @param message
     * @return
     */
    public ApiResponse<T> unauthorized(T message) {
        this.code = APICodeEnum.FAILURE;
        this.data = message;
        this.message = "unauthorized";
        return this;
    }

    /**
     * 统一身份认证暂时关闭
     *
     * @param message
     * @return
     */
    public ApiResponse<T> passPortServiceClosed(T message) {
        this.code = APICodeEnum.PASSPORT_SERVICE_CLOSED;
        this.data = message;
        this.message = "passport service is closed!";
        return this;
    }

    /**
     * 服务暂时关闭
     *
     * @param message
     * @return
     */
    public ApiResponse<T> ServiceClosed(T message) {
        this.code = APICodeEnum.SERVICE_CLOSED;
        this.data = message;
        this.message = "service is closed!";
        return this;
    }
}
