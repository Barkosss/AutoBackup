import os
import threading
from datetime import datetime
from zipfile import ZIP_DEFLATED, ZipFile

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .base_command import BaseCommand


class CreateBackupCommand(BaseCommand):
    def __init__(self) -> None:
        self.is_create: bool = False
        self.error_message: str | None = None
        self.name: str | None = None
        self.last_backup: datetime | None = None

    def get_name(self) -> str:
        return "create_backup"

    def get_description(self) -> str:
        return "Create backup"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        assert update.message is not None
        await update.message.reply_text("Backup is start create... Wait")
        thread_create_backup = threading.Thread(target=self.create_backup)
        thread_create_backup.start()
        thread_create_backup.join()
        if self.is_create:
            await update.message.reply_text(
                f"Backup is create with name: `{self.name}`",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            return

        await update.message.reply_text(
            f"Backup is not create, error:\n```{self.error_message}```",
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    def create_backup(self) -> None:
        today = datetime.now()
        format_date = today.strftime("%d-%m-%Y_%H-%M-%S")

        src_dir = os.getenv("SOURCE_DIRECTORY")
        if not src_dir:
            raise ValueError("SOURCE_DIRECTORY is not setup")

        backup_dir = os.getenv("BACKUP_DIRECTORY")
        if not backup_dir:
            raise ValueError("BACKUP_DIRECTORY is not setup")

        zip_name = f"{format_date}.zip"
        zip_path = os.path.join(backup_dir, zip_name)

        os.makedirs(backup_dir, exist_ok=True)

        try:
            with ZipFile(zip_path, "w", ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(src_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, start=src_dir)
                        zipf.write(file_path, arc_name)

            print(f"Backup created at: {zip_path}")
            self.is_create = True
            self.name = zip_name
        except Exception as err:
            self.error_message = repr(err)
