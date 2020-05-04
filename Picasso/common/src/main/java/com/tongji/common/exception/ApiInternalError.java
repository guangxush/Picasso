package com.tongji.common.exception;

/**
 * @author: guangxush
 * @create: 2020/04/13
 */
public class ApiInternalError extends RuntimeException {
    public ApiInternalError(String message, String s) {

    }

    public ApiInternalError(String message) {
        super(message);
    }

    public ApiInternalError(String message, Throwable e) {
        super(message, e);
    }
}
