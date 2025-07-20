from telegram import Update
from telegram.ext import ContextTypes

from .base_command import BaseCommand


class ListBackupCommand(BaseCommand):
    def get_name(self) -> str:
        return "list_backup"

    def get_description(self) -> str:
        return "Получить список копий"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        assert update.message is not None

        await update.message.reply_text("List backup")
