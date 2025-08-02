package com.github.barkosss.autobackupmod;

import com.github.barkosss.autobackupmod.network.HttpCommandServer;
import com.github.barkosss.autobackupmod.util.Logger;
import com.github.barkosss.autobackupmod.util.TaskScheduler;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.minecraft.server.MinecraftServer;

public class AutoBackupMod implements ModInitializer {
    public static MinecraftServer instanceServer;

    @Override
    public void onInitialize() {
        Logger.info("initializing AutoBackup");
        ServerLifecycleEvents.SERVER_STARTED.register(server -> instanceServer = server);
        HttpCommandServer.start();

        TaskScheduler.init();
    }
}
