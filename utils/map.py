from PIL import Image
from pathlib import Path

from utils.character import get_character, dying_character

_sheet = None

def _load_sheet():
    global _sheet
    if _sheet is None:
        project_root = Path(__file__).resolve().parent.parent
        sheet_path = project_root / 'assets' / 'map.png'
        _sheet = Image.open(sheet_path)
    return _sheet

def get_map(tile_index, grid_cols=15, grid_rows=15, scale=3):
    sheet = _load_sheet()
    sheet_width, sheet_height = sheet.size
    tile_width = sheet_width // grid_cols
    tile_height = sheet_height // grid_rows

    col = tile_index % grid_cols
    row = tile_index // grid_cols

    left = col * tile_width
    upper = row * tile_height
    right = left + tile_width
    lower = upper + tile_height

    tile = sheet.crop((left, upper, right, lower))
    character = get_character('119671', 7, 13, 7)
    character = dying_character(character)
    tile.paste(character, (50, 70), character)

    new_size = (tile_width * scale, tile_height * scale)
    return tile.resize(new_size, resample=Image.NEAREST)