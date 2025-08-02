package com.github.barkosss.autobackupmod.commands;

import com.github.barkosss.autobackupmod.AutoBackupMod;
import com.github.barkosss.autobackupmod.enums.HttpMethods;
import com.github.barkosss.autobackupmod.util.Logger;
import com.github.barkosss.autobackupmod.util.TaskScheduler;
import net.minecraft.entity.boss.BossBar;
import net.minecraft.entity.boss.ServerBossBar;
import net.minecraft.network.message.SignedMessage;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.network.message.SentMessage;
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

        server.(Text.literal("Сервер через минуту будет закрыт для создания бэкапа!"));

        for (ServerPlayerEntity player : players) {
            bossBar.addPlayer(player);
            player.sendChatMessage(, true);

            TaskScheduler.schedule(() -> {
                bossBar.removePlayer(player);
                // ...
            }, 1200); // 1 минута
        }
    }
}
