import os
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from .base_command import BaseCommand
from .list_backup import ListBackupCommand

WAITING_FOR_INPUT = 1


class RemoveBackupCommand(BaseCommand):
    def get_name(self) -> str:
        return "remove_backup"

    def get_description(self) -> str:
        return "Remove Backup"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        assert update.message is not None
        args: list[str] = update.message.text.split(" ")[1:]
        if (update.message is not None) and len(args):
            await self.remove(update=update, backup_name=args[0])
            return ConversationHandler.END
        else:
            await update.message.reply_text("Enter backup's name")
            return WAITING_FOR_INPUT

    @staticmethod
    async def remove(update: Update, backup_name: str) -> int:
        assert update.message is not None
        backup_name = backup_name.lower()
        backups: list[str] = ListBackupCommand.get_backups()

        if not (backup_name.endswith(".zip")):
            backup_name += ".zip"

        # If backup name is not found is backups list
        if not (backup_name in backups):
            await update.message.reply_text(
                f'Backup "{backup_name}" not found. Enter backup\'s name again'
            )
            return WAITING_FOR_INPUT

        backup: Path = Path(os.getenv("BACKUP_DIRECTORY") + "/" + backup_name)
        backup.unlink()
        await update.message.reply_text(f'Backup "{backup_name}" is remove')
        return ConversationHandler.END
