import io
import re
from irispy2 import ChatContext
from utils.map import get_map

invoke = "맵"

maps = [
    {'id':120, 'name':'공원'},
    {'id':123, 'name':'백화점'},
]



def handle(event:ChatContext):
    if event.message.msg == '!맵':
        lines = [f"{i}. {m['name']}" for i, m in enumerate(maps, start=1)]
        event.reply("'!맵 <번호>'를 입력해주세요.\n"+"\n".join(lines))

    m = re.match(r"^!맵\s*(\d+)", event.message.msg)
    if not m: return
    num = int(m.group(1))
    tile = get_map(maps[num-1]['id'])
    buf = io.BytesIO()
    tile.save(buf, format="PNG")
    buf.seek(0)
    event.reply_media(
        "IMAGE",
        [buf],
    )
