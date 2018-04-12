import hashlib
import os

from django.conf import settings

from PIL import Image, ImageColor, ImageDraw, ImageFont


FULLSIZE = 120 * 3
POINTSIZE = 280
OFFSET_Y = 47

COLORS = ["871f22", "59e747", "a44af3", "7deb36", "4937d2", "b0ef26",
          "731cbe", "a5e841", "c441e9", "56ea6d", "e450ea", "38b931", "e431cb",
          "e1ec2c", "7c51e7", "84c831", "b422bc", "90ea66", "344dd6", "c4e143",
          "8540c9", "5da929", "b161f1", "37d275", "ea2db9", "76f696", "331484",
          "edd53f", "7227a3", "bfec6f", "ce3fc3", "35f4b5", "eb2ba2", "37ae55",
          "be55d4", "3e8e1a", "9c5ad7", "dce358", "6368e7", "eabc27", "4f83f7",
          "f02f14", "55f4df", "e6252a", "47e4bb", "bc1794", "6ec660", "ee53be",
          "1e933c", "e96fdf", "88a721", "4f42ab", "c4b734", "2f65d0", "e6a232",
          "2e8bf3", "e44410", "41d6eb", "eb5916", "4c93e9", "e88022", "a978ee",
          "94c452", "ce45b2", "6bdd8c", "a82b90", "4ccb8a", "e7388b", "83f1b4",
          "94359b", "96e38e", "5f2078", "e4e377", "292572", "c7e78e", "310d53",
          "a2af3e", "af5bc3", "468d33", "da83ed", "2b6619", "c46fd8", "3d8d47",
          "ef4378", "41b584", "ea3961", "40c7b6", "f35335", "6ae7e6", "c71f31",
          "94edc7", "761268", "c4f0b2", "ab1d69", "308e59", "c32464", "1d9879",
          "e94147", "61c5e6", "c53616", "5eb1e5", "e86c39", "7d88ed", "b68f1e",
          "4766bc", "c7b556", "845ab7", "62852b", "ea88e2", "134b18", "e777c3",
          "8faf5a", "bf60b8", "808221", "917bdc", "c37424", "30428c", "ebdb8b",
          "1e1e4e", "e9f2c6", "32133c", "accf93", "9e2e7d", "6fac6c", "cc55a5",
          "7dcc9f", "dc508e", "5c844c", "bd8ce9", "586419", "d999e1", "3a4a12",
          "efb2f0", "193112", "ed76b1", "3d6b3f", "f1615f", "398fbf", "9f2f14",
          "a4e1ec", "a42243", "afe7d3", "340a29", "e9be76", "19132a", "e9d6aa",
          "5f2056", "cdd3a1", "663b7f", "ca9c4d", "8c88d7", "967724", "6a91d7",
          "c1532c", "3270a7", "ea6e4f", "4ca1c0", "cf504e", "6ebdb9", "c8455d",
          "34909a", "a33c33", "a6d1f5", "631c10", "cde8e2", "480b1f", "efdad1",
          "0f202b", "e59855", "485c97", "995719", "8eb1e9", "924521", "c3b2eb",
          "673a12", "dbccee", "311717", "becede", "6a1928", "609e87", "7f2157",
          "bcbc7c", "915190", "ac9c58", "493f6c", "f2936d", "265582", "d56b58",
          "2d664b", "eb709a", "324a2a", "b778b9", "8fa774", "751840", "c5cebb",
          "3c1829", "eab589", "272a42", "c7b486", "ad4c80", "447f6d", "e9767e",
          "2c5854", "e592b5", "252d21", "edb7d3", "443815", "8f8ac5", "755b26",
          "6d8ebb", "c17449", "274354", "e89098", "3e5c70", "c78f66", "7e6499",
          "9f763e", "6f6e97", "888a59", "a43d63", "99b3a1", "652f49", "89b4c7",
          "592b22", "a6a9c8", "4d3221", "ddb8a1", "573f56", "e4a294", "567b99",
          "ba595f", "5c6235", "c06e92", "6e8274", "873c48", "6a818e", "b56658",
          "a88eae", "813f34", "c9a9af", "503c41", "a6967c", "965774", "595948",
          "c47c8d", "745e41", "98728f", "925a3e", "786179", "a87962", "7d525f",
          "b58982", "76544f", "ac7e8b", "a36365", "8e7975"]


def generate_avatar(letter, data, size=FULLSIZE):
    if size > FULLSIZE:
        size = FULLSIZE

    # Determine color
    h = hashlib.sha256()
    h.update(data.encode('utf-8'))

    color = int(h.hexdigest()[0:16], 16) % 256
    bg_color = ImageColor.getrgb('#' + COLORS[color])

    # Create image
    img = Image.new('RGBA', (FULLSIZE, FULLSIZE), bg_color + (255, ))

    font_path = os.path.join(settings.MEDIA_ROOT, 'fonts/Helvetica.ttf')
    font = ImageFont.truetype(font_path, POINTSIZE)
    font_color = (bg_color) + (0x33, )

    draw = ImageDraw.Draw(img)
    text_size = draw.textsize(letter.upper(), font=font)
    position = ((FULLSIZE - text_size[0]) / 2,
                (FULLSIZE - OFFSET_Y - text_size[1]) / 2)
    draw.text(position, letter.upper(), font=font, fill=font_color)

    dir_path = 'avatars/letter/' + letter.lower() + '/' + COLORS[color] + '/'
    file_name = str(size) + '.png'

    image_path = os.path.join(settings.MEDIA_ROOT, dir_path)
    try:
        os.makedirs(image_path, 0o755)
    except OSError:
        pass
    # Create image
    image_path = os.path.join(image_path, file_name)
    img.save(image_path, 'PNG')

    # Return URL
    file_url = os.path.join(settings.MEDIA_URL, dir_path)
    file_url = os.path.join(file_url, file_name)
    return file_url
