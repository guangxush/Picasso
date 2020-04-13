package com.tongji.common.exception;

/**
 * @author: guangxush
 * @create: 2020/04/13
 */
public class AppInternalError extends RuntimeException {
    public AppInternalError(String message, String s) {

    }

    public AppInternalError(String message) {
        super(message);
    }

    public AppInternalError(String message, Throwable e) {
        super(message, e);
    }
}
