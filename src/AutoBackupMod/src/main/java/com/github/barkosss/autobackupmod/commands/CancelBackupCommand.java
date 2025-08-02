package com.github.barkosss.autobackupmod.commands;

import com.github.barkosss.autobackupmod.enums.HttpMethods;

import java.util.Map;

public class CancelBackupCommand implements BaseCommand {

    @Override
    public String getName() {
        return "cancel";
    }

    @Override
    public HttpMethods getMethod() {
        return HttpMethods.POST;
    }

    @Override
    public void execute(Map<String, String> query) {
        System.out.println("Cancel backup command");
    }
}
