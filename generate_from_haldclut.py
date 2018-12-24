import json
import os
import subprocess
from PIL import Image


CLASSIC_PNG = '/tmp/classic.png'
PROCESSED_PNG = '/tmp/processed.png'
CLUTS_DIR = './cluts'
SCHEMES_DIR = './styles/schemes'
CLUT_THEMES_JSON = './lib/clut-themes.json'
WHITELIST_TXT = './clut_whitelist.txt'

classic_monokai = {
    'background': '#272821',
    'neutral': '#6e7066',
    'foreground': '#fdfff1',
    'red': '#f82570',
    'orange': '#fc961f',
    'yellow': '#e4db73',
    'green': '#a6e12d',
    'cyan': '#66d9ee',
    'purple': '#ae81ff',
}


def hex_to_rgb(hex_color):
    return [
        int(hex_color[1:3], 16),
        int(hex_color[3:5], 16),
        int(hex_color[5:7], 16)
    ]


def rgb_to_hex(rgb_color):
    output = '#'
    for component in rgb_color:
        output += format(component, '02x')
    return output


def scheme_to_pixels(scheme):
    output = []
    for name, hex_color in scheme.items():
        output += hex_to_rgb(hex_color)
    return bytes(output)


def decamelize_name(name):
    output = ''
    for idx, x in enumerate(name):
        if idx > 0:
            prev = name[idx - 1]
            if (
                prev.isalnum()
                and (x.isupper() or x.isdigit())
                and prev.islower()
            ):
                output += f' {x}'
                continue
        output += x
    return output


def generate_schemes():
    with open(WHITELIST_TXT, 'r') as fp:
        whitelist = fp.read().splitlines()
    generated_names = []
    for sub_directory in os.listdir(CLUTS_DIR):
        for clut_filename in os.listdir(
            os.path.join(CLUTS_DIR, sub_directory)
        ):
            name = decamelize_name(clut_filename[:-4])
            if sub_directory.startswith('CreativePack'):
                name = f'CP {name}'
            if name not in whitelist:
                continue

            classic_img = Image.frombytes(
                'RGB',
                (len(classic_monokai), 1),
                scheme_to_pixels(classic_monokai)
            )
            classic_img.save(CLASSIC_PNG)

            cmd = [
                'gm', 'convert', CLASSIC_PNG,
                '-hald-clut', os.path.join(
                    CLUTS_DIR, sub_directory, clut_filename
                ),
                PROCESSED_PNG
            ]
            subprocess.Popen(cmd).wait()
            processed_image = Image.open(PROCESSED_PNG)

            less_scheme = ''
            for idx, color_name in enumerate(classic_monokai):
                rgb_pixel = processed_image.getpixel((idx, 0))
                hex_color = rgb_to_hex(rgb_pixel)
                less_scheme += f'@{color_name}: {hex_color};\n'

            name_normalized = name.replace(' ', '-').lower()
            scheme_filename = f'{name_normalized}.less'
            with open(os.path.join(SCHEMES_DIR, scheme_filename), 'w') as fp:
                fp.write(less_scheme)
            generated_names.append(name)

    return generated_names


if __name__ == '__main__':
    names = generate_schemes()
    with open(CLUT_THEMES_JSON, 'w') as fp:
        json.dump(names, fp)
