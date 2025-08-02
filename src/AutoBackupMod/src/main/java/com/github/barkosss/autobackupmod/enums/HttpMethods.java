package com.github.barkosss.autobackupmod.enums;

public enum HttpMethods {
    GET("GET"),
    POST("POST"),
    PUT("PUT"),
    PATCH("PATCH"),
    DELETE("DELETE"),
    HEAD("HEAD"),
    OPTIONS("OPTIONS");

    private final String method;

    HttpMethods(String method) {
        this.method = method;
    }

    public String getMethodName() {
        return method;
    }
}
