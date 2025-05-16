import io
import re
from irispy2 import ChatContext

from utils.character import get_character, dying_character

invoke = "캐릭터"



def handle(event:ChatContext):
    m = re.match(r"^!캐릭터\s*(\d+)", event.message.msg)
    if not m: return
    num = int(m.group(1))
    tile = get_character('119671',7,13,7)
    tile = dying_character(tile)

    buf = io.BytesIO()
    tile.save(buf, format="PNG")
    buf.seek(0)
    event.reply_media(
        "IMAGE",
        [buf],
    )
