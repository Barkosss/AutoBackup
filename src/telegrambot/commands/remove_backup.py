from telegram import Update
from telegram.ext import ContextTypes

from .base_command import BaseCommand


class RemoveBackupCommand(BaseCommand):
    def get_name(self) -> str:
        return "remove_backup"

    def get_description(self) -> str:
        return "Удалить резервное копирование"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        assert update.message is not None

        await update.message.reply_text("Remove backup")
