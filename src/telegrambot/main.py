import importlib
import inspect
import logging
import os
import pkgutil

from commands.base_command import BaseCommand
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def discovery_commands(package_name: str) -> list[BaseCommand]:
    commands: list[BaseCommand] = []

    package = importlib.import_module(package_name)
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseCommand) and obj is not BaseCommand:
                commands.append(obj())

    return commands


def main() -> None:
    token = os.getenv("TELEGRAM_TOKEN")
    if token is None:
        raise ValueError("TELEGRAM_TOKEN not set")
    application = Application.builder().token(token).build()
    commands: list[BaseCommand] = discovery_commands("commands")
    for command in commands:

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
