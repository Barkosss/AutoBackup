from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes

from .base_command import BaseCommand


class ReloadCommand(BaseCommand):
    def get_name(self) -> str:
        return "reload"

    def get_description(self) -> str:
        return "Reload env config"

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        assert update.message is not None
        load_dotenv(override=True)
        await update.message.reply_text("Env is reload!")
