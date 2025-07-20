from base_command import BaseCommand

from telegram import Update
from telegram.ext import ContextTypes


class HelpCommand(BaseCommand):
    def get_name(self) -> str:
        return "help"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        pass
