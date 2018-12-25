import colorsys
import os
import jinja2
import json
from generate_from_haldclut import (
    hex_to_rgb, SCHEMES_DIR, CLUT_THEMES_JSON
)
MONOKAI_THEMES_JSON = './lib/monokai-themes.json'
PREVIEWS_DIR = './previews'

README_TEMPLATE = 'README-template.md'

template_loader = jinja2.FileSystemLoader(searchpath='./')
env = jinja2.Environment(
    loader=template_loader,
    trim_blocks=True,
    lstrip_blocks=True
)
TEMPLATE_FILE = 'preview-template.svg'


def prepare_theme_data(theme_name):
    normalized = theme_name.replace(' ', '-').lower()
    less_colors = []
    with open(os.path.join(SCHEMES_DIR, f'{normalized}.less'), 'r') as fp:
        for line in fp.read().splitlines():
            less_colors.append(f"#{line.split('#')[1][:6]}")
    colors = [{
        'hex': color,
        'hsv': colorsys.rgb_to_hsv(*list(map(
            lambda x: x / 255,
            hex_to_rgb(color)
        )))
    } for color in less_colors]

    return {
        'name': theme_name,
        'slug': normalized,
        'colors': colors
    }


def render_preview(groups):
    template = env.get_template(TEMPLATE_FILE)
    with open('preview.svg', 'w') as fp:
        fp.write(template.render(groups=groups))


if __name__ == '__main__':
    theme_names = []
    with open(CLUT_THEMES_JSON, 'r') as fp:
        theme_names += json.load(fp)
    with open(MONOKAI_THEMES_JSON, 'r') as fp:
        theme_names += json.load(fp)

    themes = []
    for theme_name in theme_names:
        data = prepare_theme_data(theme_name)
        themes.append(data)

    groups = list(zip(*(iter(themes),) * 3)) 

    render_preview(groups)
