package com.github.barkosss.autobackupmod.commands;

import com.github.barkosss.autobackupmod.enums.HttpMethods;

import java.util.Map;

public interface BaseCommand {

    String getName();

    HttpMethods getMethod();

    void execute(Map<String, String> query);
}
