from PIL import Image, ImageDraw, ImageFont
import numpy as np

from generator import create_consistent_field

CELL_WIDTH = 25
OPEN_CELL_COLOR = "#E3E2DF"
CLOSE_CELL_COLOR = "#E3AFBC"  # 9A1750, EE4C7C


def model(field: np.ndarray, hidden: bool = False):
    v, h = field.shape

    img_v = v * CELL_WIDTH
    img_h = h * CELL_WIDTH

    img: Image = Image.new("RGBA", (img_h, img_v), OPEN_CELL_COLOR)
    mine_img: Image = Image.open("mine.png")
    mine_img = mine_img.resize((CELL_WIDTH - 11, CELL_WIDTH - 11))

    draw: ImageDraw = ImageDraw.Draw(img)

    for xi, x in enumerate(range(0, img_h, CELL_WIDTH)):
        for yi, y in enumerate(range(0, img_v, CELL_WIDTH)):
            x0, y0 = x + 2, y + 2
            x1, y1 = x + CELL_WIDTH - 3, y + CELL_WIDTH - 3

            msg = str(field[yi][xi])

            draw.rounded_rectangle(
                [x0, y0, x1, y1],
                radius=5,
                fill=OPEN_CELL_COLOR if msg != '-1' else CLOSE_CELL_COLOR,
                outline=CLOSE_CELL_COLOR
            )

            font: ImageFont = ImageFont.truetype('arial.ttf', 12)

            xc = x + (CELL_WIDTH // 2)
            yc = y + (CELL_WIDTH // 2)

            if msg == '-1':
                img.paste(mine_img,
                          (x + 5, y + 5, x + CELL_WIDTH - 6, y + CELL_WIDTH - 6),
                          mine_img)

            elif msg != '0':
                draw.text((xc, yc),
                          text=msg,
                          font=font,
                          fill=CLOSE_CELL_COLOR,
                          anchor='mm')

    return img


if __name__ == '__main__':
    field, mines = create_consistent_field(30, 16)
    model(field).save('test.png')
