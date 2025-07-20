from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import ContextTypes


class BaseCommand(ABC):
    @abstractmethod
    def get_name(self) -> str:
        """

        :return: str - name of command
        """
        pass

    @abstractmethod
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """

        :return:
        """
        pass
