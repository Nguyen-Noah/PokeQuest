import os, json
from PIL import Image

folder_path = './data/pokemon/'
postfix = '/sprites/back_default.png'

for folder in os.listdir(folder_path):
    offset = None
    with Image.open(f'{folder_path}{folder}{postfix}') as img:
        w, h = img.size

        for y in range(h-1, -1, -1):
            for x in range(w):
                pixel = img.getpixel((x, y))

                if pixel[3] == 255:
                    offset = y
                    print(f'{folder}: First pixel found at {(x, y)}')
                    break

            if offset:
                config = {'alpha_offset': offset}
                f = open(f'{folder_path}/{folder}/sprites/sprite_config.json', 'w')
                f.write(json.dumps(config))
                f.close()
                break

    img.close()