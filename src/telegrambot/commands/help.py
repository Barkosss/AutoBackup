import inspect

from telegram import Update
from telegram.ext import ContextTypes

from .base_command import BaseCommand


class HelpCommand(BaseCommand):
    def get_name(self) -> str:
        return "help"

    def get_description(self) -> str:
        return "A guide to commands"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        assert update.message is not None
        message_lines: list[str] = ["====== HELP ======\n"]
        for command in _get_command_list(BaseCommand):
            message_lines.append(
                f" - /{command.get_name()}\n\t{command.get_description()}\n"
            )

        message: str = "\n".join(message_lines)
        await update.message.reply_text(message)


def _get_all_subclasses(cls: type) -> set[type]:
    subclasses = set()
    for subclass in cls.__subclasses__():
        subclasses.add(subclass)
        subclasses.update(_get_all_subclasses(subclass))
    return subclasses


def _get_command_list(base_cls: type) -> list[BaseCommand]:
    commands = []
    for cls in _get_all_subclasses(base_cls):
        if not inspect.isabstract(cls) and issubclass(cls, BaseCommand):
            commands.append(cls())
    return commands
