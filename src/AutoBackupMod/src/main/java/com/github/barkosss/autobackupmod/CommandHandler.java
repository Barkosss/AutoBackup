package com.github.barkosss.autobackupmod;

import com.github.barkosss.autobackupmod.commands.BaseCommand;
import com.github.barkosss.autobackupmod.util.Logger;
import com.github.barkosss.autobackupmod.util.QueryUtils;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import org.reflections.Reflections;

import java.io.IOException;
import java.io.OutputStream;
import java.net.URI;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class CommandHandler implements HttpHandler {
    private static final Map<String, BaseCommand> commands = new HashMap<>();

    public void init() {
        Logger.debug("Initializing CommandHandler");

        try {
            Reflections reflections = new Reflections();
            Set<Class<? extends BaseCommand>> subclasses = reflections.getSubTypesOf(BaseCommand.class);
            Logger.info("Found " + subclasses.size() + " commands classes");

            String commandName;
            BaseCommand instanceClass;

            for (Class<? extends BaseCommand> subclass : subclasses) {
                instanceClass = subclass.getConstructor().newInstance();
                commandName = instanceClass.getName().toLowerCase();
                Logger.debug("Trying to load command: " + commandName);

                if (commandName.isEmpty()) {
                    Logger.warn("Skipped command with empty name: " + subclass.getSimpleName());
                    continue;
                }

                if (!commands.containsKey(commandName)) {
                    commands.put(commandName, instanceClass);
                    Logger.info("Command registered: " + commandName);
                    continue;
                }

                String errMessage = String.format("There was a duplication of the command - %s", commandName);
                Logger.error(errMessage);
                System.exit(501);
            }

            Logger.info("CommandHandler initialized successfully");

        } catch (Exception ex) {
            Logger.error("Command loader: " + ex.getMessage());
        }
    }

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        if (!exchange.getRequestMethod().equalsIgnoreCase("POST")) {
            // Method is not supported
            exchange.sendResponseHeaders(405, -1);
        }

        URI uri = exchange.getRequestURI();
        String commandMethod = exchange.getRequestMethod().toLowerCase();
        String commandName = uri.getPath().substring(1);
        String query = uri.getQuery();

        Logger.info("Get REST-command: " + commandName);
        if (commands.containsKey(commandName)) {
            BaseCommand command = commands.get(commandName);

            if (!command.getMethod().getMethodName().equalsIgnoreCase(commandMethod)) {
                Logger.debug("Method is not supported by command: /" + commandName);
                exchange.sendResponseHeaders(405, -1);
                return;
            }

            command.execute(QueryUtils.queryToMap(query));
            String response = "Command complete: " + commandName;
            byte[] responseBytes = response.getBytes();
            exchange.sendResponseHeaders(200, responseBytes.length);
            OutputStream os = exchange.getResponseBody();
            os.write(responseBytes);
            os.close();
            return;
        }

        String response = "Command received: " + commandName;
        byte[] responseBytes = response.getBytes();
        exchange.sendResponseHeaders(404, responseBytes.length);
        OutputStream os = exchange.getResponseBody();
        os.write(responseBytes);
        os.close();
    }
}
