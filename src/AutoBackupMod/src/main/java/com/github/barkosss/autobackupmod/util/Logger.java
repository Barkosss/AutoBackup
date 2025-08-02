package com.github.barkosss.autobackupmod.util;

import org.slf4j.LoggerFactory;

public class Logger {
    private static final org.slf4j.Logger LOGGER = LoggerFactory.getLogger("AutoBackup");
    private static final String PREFIX = "[AutoBackup]";

    public static void info(String msg, Object... args) {
        LOGGER.info(String.format("%s %s", PREFIX, msg), args);
    }

    public static void warn(String msg, Object... args) {
        LOGGER.warn(String.format("%s %s", PREFIX, msg), args);
    }

    public static void error(String msg, Object... args) {
        LOGGER.error(String.format("%s %s", PREFIX, msg), args);
    }

    public static void debug(String msg, Object... args) {
        LOGGER.debug(String.format("%s %s", PREFIX, msg), args);
    }
}