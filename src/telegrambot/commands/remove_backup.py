from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from .base_command import BaseCommand

WAITING_FOR_NAME = 1

class RemoveBackupCommand(BaseCommand):
    def get_name(self) -> str:
        return "remove_backup"

    def get_description(self) -> str:
        return "Delete Backup"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        assert update.message is not None

        await update.message.reply_text("Remove backup")
        return WAITING_FOR_NAME

    @staticmethod
    async def remove(update: Update, backup_name: str) -> int:
        assert update.message is not None

        await update.message.reply_text(f"Text={backup_name}")
        return ConversationHandler.END
