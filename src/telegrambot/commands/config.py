from telegram import Update
from telegram.ext import ContextTypes

from .base_command import BaseCommand


class ConfigCommand(BaseCommand):
    def get_name(self) -> str:
        return "config"

    def get_description(self) -> str:
        return "Configure Telegram Bot"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        assert update.message is not None
