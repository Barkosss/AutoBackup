package com.github.barkosss.autobackupmod.commands;

import com.github.barkosss.autobackupmod.AutoBackupMod;
import com.github.barkosss.autobackupmod.enums.HttpMethods;
import com.github.barkosss.autobackupmod.util.Logger;
import com.github.barkosss.autobackupmod.util.TaskScheduler;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.minecraft.entity.boss.BossBar;
import net.minecraft.entity.boss.ServerBossBar;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.text.Text;

import java.util.List;
import java.util.Map;

/**
 *
 */
public class CreateBackupCommand implements BaseCommand {

    @Override
    public String getName() {
        return "create";
    }

    @Override
    public HttpMethods getMethod() {
        return HttpMethods.POST;
    }

    @Override
    public void execute(Map<String, String> query) {
        register();
        Logger.debug("Create backup");

        MinecraftServer server = AutoBackupMod.instanceServer;
        List<ServerPlayerEntity> players = server.getPlayerManager().getPlayerList();
        ServerBossBar bossBar = new ServerBossBar(
                Text.of("Создание бэкапа..."),
                BossBar.Color.BLUE,
                BossBar.Style.PROGRESS
        );

        bossBar.setPercent(1.0f);
        bossBar.setVisible(true);

        Text text = Text.literal("Сервер через минуту будет закрыт для создания бэкапа!");
        for (ServerPlayerEntity player : players) {
            bossBar.addPlayer(player);
            player.sendMessage(text, true);

            TaskScheduler.schedule(() -> {
                bossBar.removePlayer(player);
                player.networkHandler.disconnect(Text.literal("Сервер выключается для перезапуска"));
            }, 1200); // 1 минута
        }
    }

    private void register() {
        ServerPlayConnectionEvents.DISCONNECT.register(((handler, server) -> {
            if (!server.getPlayerManager().getPlayerList().isEmpty()) {
                return;
            }

            Logger.info("Server is stop");
            server.stop(true);
        }));
    }
}
