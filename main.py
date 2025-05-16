from irispy2 import Bot, ChatContext
from irispy2.bot.models import ErrorContext

from command.command_manager import CommandManager

bot = Bot(iris_url="http://140.238.8.198:3000")
manager = CommandManager()

@bot.on_event("message")
def on_message(chat: ChatContext):
    manager.handle_command(chat)

@bot.on_event("error")
def on_error(err: ErrorContext):
    print(err.event, "이벤트에서 오류가 발생했습니다", err.exception)

if __name__ == "__main__":
    bot.run()