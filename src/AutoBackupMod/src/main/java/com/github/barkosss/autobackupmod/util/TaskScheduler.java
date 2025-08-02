package com.github.barkosss.autobackupmod.util;

import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;

import java.util.Iterator;
import java.util.LinkedList;

public class TaskScheduler {
    private static final LinkedList<ScheduledTask> tasks = new LinkedList<>();

    public static void init() {
        ServerTickEvents.START_SERVER_TICK.register(server -> {
            Iterator<ScheduledTask> iterator = tasks.iterator();
            while (iterator.hasNext()) {
                ScheduledTask task = iterator.next();
                if (--task.ticks <= 0) {
                    task.runnable.run();
                    iterator.remove();
                }
            }
        });
    }

    public static void schedule(Runnable runnable, int delayTicks) {
        tasks.add(new ScheduledTask(runnable, delayTicks));
    }

    private static class ScheduledTask {
        Runnable runnable;
        int ticks;

        ScheduledTask(Runnable runnable, int ticks) {
            this.runnable = runnable;
            this.ticks = ticks;
        }
    }
}