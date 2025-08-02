package com.github.barkosss.autobackupmod.commands;

import com.github.barkosss.autobackupmod.enums.HttpMethods;

import java.util.Map;

public class RemoveBackupCommand implements BaseCommand {

    @Override
    public String getName() {
        return "remove";
    }

    @Override
    public HttpMethods getMethod() {
        return HttpMethods.POST;
    }

    @Override
    public void execute(Map<String, String> query) {
        System.out.println("Remove backup");
    }
}
