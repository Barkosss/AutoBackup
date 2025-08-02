import importlib
import inspect
import logging
import os
import pkgutil

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from commands.base_command import BaseCommand
from commands.help import HelpCommand
from commands.remove_backup import RemoveBackupCommand

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

WAITING_FOR_INPUT = 1


def discovery_commands(package_name: str) -> list[BaseCommand]:
    commands: list[BaseCommand] = []

    package = importlib.import_module(package_name)
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseCommand) and obj is not BaseCommand:
                commands.append(obj())

    return commands


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message is not None
    assert update.message.text is not None
    await RemoveBackupCommand.remove(update=update, backup_name=update.message.text)
    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await HelpCommand().execute(update=update, context=context)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message is not None

    await update.message.reply_text("Action is cancel")
    return ConversationHandler.END


def main() -> None:
    token = os.getenv("TELEGRAM_TOKEN")
    if token is None:
        raise ValueError("TELEGRAM_TOKEN not set")
    application = Application.builder().token(token).build()
    commands: list[BaseCommand] = discovery_commands("commands")
    for command in commands:
        if isinstance(command, RemoveBackupCommand):
            conv_handler = ConversationHandler(
                entry_points=[
                    CommandHandler(
                        command.get_name(), lambda u, c: command.execute(u, c)
                    )
                ],
                states={
                    WAITING_FOR_INPUT: [
                        MessageHandler(filters.TEXT & ~filters.COMMAND, text)
                    ],
                },
                fallbacks=[CommandHandler("cancel", cancel)],
            )
            application.add_handler(conv_handler)
        else:

            async def handler(
                    update: Update,
                    context: ContextTypes.DEFAULT_TYPE,
                    cmd: BaseCommand = command,
            ) -> None:
                await cmd.execute(update, context)

            application.add_handler(CommandHandler(command.get_name(), handler))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    load_dotenv()
    main()
