import json
import os

from PIL import Image
from pathlib import Path

from utils.palette import ColorType


def _load_sheet(character_id):
    _sheet = None
    if _sheet is None:
        project_root = Path(__file__).resolve().parent.parent
        sheet_path = project_root / 'assets' / 'characters' / f'{character_id}.png'
        _sheet = Image.open(sheet_path)
    return _sheet

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# JSON 파일과 이미지 파일의 경로
json_path = os.path.join(BASE_DIR, "assets" ,"characters","character_position.json")

def get_character(character_id, eye_index, body_index, acc_index):
    data = None
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    img = _load_sheet(character_id)
    eye = data['sprites']['eyes'][eye_index]
    body = data['sprites']['body'][body_index]
    acc = data['sprites']['acc'][acc_index]

    eye_x, eye_y, eye_w, eye_h = eye["x"], eye["y"], eye["width"], eye["height"]
    body_x, body_y, body_w, body_h = body["x"], body["y"], body["width"], body["height"]
    acc_x, acc_y, acc_w, acc_h = acc["x"], acc["y"], acc["width"], acc["height"]

    eye_cropped = img.crop((eye_x, eye_y, eye_x + eye_w, eye_y + eye_h)).convert("RGBA")
    body_cropped = img.crop((body_x, body_y, body_x + body_w, body_y + body_h)).convert("RGBA")
    acc_cropped = img.crop((acc_x, acc_y, acc_x + acc_w, acc_y + acc_h)).convert("RGBA")

    combined = Image.new("RGBA", body_cropped.size, (0, 0, 0, 0))  # 완전 투명 배경
    combined.paste(body_cropped, (0, 0), body_cropped)  # 바디 먼저 붙임
    combined.paste(eye_cropped, (7, 15), eye_cropped)  # 눈을 위에 붙임
    combined.paste(acc_cropped, (5, -8), acc_cropped)

    return combined

def dying_character(img):
    target_color = (222, 219, 197, 255)  # 바꿀 색 (예: 노란색)
    replacement = (ColorType.Yellow.value[0], ColorType.Yellow.value[1], ColorType.Yellow.value[2], 255)  # 새로운 색 (예: 초록색)

    width, height = img.size

    img = img.convert("RGBA")
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            if pixels[x, y] == target_color:
                pixels[x, y] = replacement

    return img
