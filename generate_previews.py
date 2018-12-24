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
template = env.get_template(TEMPLATE_FILE)


def generate_preview(theme_name):
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

    with open(os.path.join(PREVIEWS_DIR, f'{normalized}.svg'), 'w') as fp:
        fp.write(template.render(colors=colors))
    return normalized


if __name__ == '__main__':
    theme_names = []
    with open(CLUT_THEMES_JSON, 'r') as fp:
        theme_names += json.load(fp)
    with open(MONOKAI_THEMES_JSON, 'r') as fp:
        theme_names += json.load(fp)

    themes = []
    for theme_name in theme_names:
        normalized = generate_preview(theme_name)
        themes.append({
            'name': theme_name,
            'slug': normalized.replace('(', '%28').replace(')', '%29')
        })

    themes = zip(*(iter(themes),) * 3)
    readme_template = env.get_template(README_TEMPLATE)
    with open('README.md', 'w') as fp:
        fp.write(readme_template.render(themes=themes))
