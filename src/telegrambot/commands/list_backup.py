import os

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .base_command import BaseCommand


class ListBackupCommand(BaseCommand):
    def get_name(self) -> str:
        return "list_backup"

    def get_description(self) -> str:
        return "Get a list of copies"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        assert update.message is not None

        backups: list[str] = self.get_backups()
        message: str = "\\=\\=\\=\\=\\=\\= LIST \\=\\=\\=\\=\\=\\=\n\n"
        for index, file_name in enumerate(backups):
            message += f"{index + 1}\\. `{file_name}`\n"
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)

    @staticmethod
    def get_backups() -> list[str]:
        backups: list[str] = []
        with os.scandir(os.getenv("BACKUP_DIRECTORY")) as entries:
            for entry in entries:
                if entry.is_file():
                    backups.append(entry.name)
        return backups
