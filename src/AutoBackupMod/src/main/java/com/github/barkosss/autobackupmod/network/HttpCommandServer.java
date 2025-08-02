package com.github.barkosss.autobackupmod.network;

import com.github.barkosss.autobackupmod.CommandHandler;
import com.github.barkosss.autobackupmod.util.Logger;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.net.InetSocketAddress;

public class HttpCommandServer {

    public static void start() {
        try {
            CommandHandler commandHandler = new CommandHandler();
            commandHandler.init();
            
            HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
            server.createContext("/", commandHandler);
            server.setExecutor(null);
            server.start();
            Logger.info("REST API is start on port 8080");

        } catch (IOException exception) {
            Logger.debug("REST API Error: " + exception.getMessage());
        }
    }
}
