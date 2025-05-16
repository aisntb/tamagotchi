import os
import importlib
from irispy2 import ChatContext

class CommandManager:
    def __init__(self):
        self.exact_commands = {}
        self.prefix = "!"

        print("🔄 명령어 로딩 중...")
        self.load_commands()

    def load_commands(self):
        current_dir = os.path.dirname(__file__)
        command_dir = os.path.join(current_dir, "commands")

        for filename in os.listdir(command_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"command.commands.{filename[:-3]}"
                try:
                    print(f"⏳ importing {module_name}")
                    module = importlib.import_module(module_name)
                    invoke = getattr(module, "invoke", None)
                    handle = getattr(module, "handle", None)

                    if invoke and handle:
                        self.exact_commands[invoke.lower()] = handle
                        print(f"☀️ 명령어 등록: {invoke.lower()}")
                    else:
                        print(f"⚠️ {module_name}에서 invoke나 handle이 없음")
                except Exception as e:
                    print(f"❌ {module_name} 로드 실패: {e}")

    def handle_command(self, event: ChatContext):
        if not event.message.msg.startswith(self.prefix):
            return

        content = event.message.msg[len(self.prefix):].strip()
        if not content:
            return

        split = content.split()
        invoke = split[0].lower()

        handler = self.exact_commands.get(invoke)
        if handler:
            try:
                handler(event)
            except Exception as e:
                event.reply(f"명령어 실행 중 오류 발생: {e}")
