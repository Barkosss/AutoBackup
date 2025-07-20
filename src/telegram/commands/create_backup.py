# import os
# import threading

from base_command import BaseCommand

from telegram import Update
from telegram.ext import ContextTypes


class CreateBackup(BaseCommand):
    def get_name(self) -> str:
        return "create_backup"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        pass
