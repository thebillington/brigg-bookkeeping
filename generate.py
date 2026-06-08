#!/usr/bin/env python3
from datetime import datetime
import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import shutil

ROOT = Path(__file__).parent
DATA = ROOT / "data"
TEMPLATES = ROOT / "templates"
OUTPUT = ROOT / "output"
IMAGES = ROOT / "images"

DATA_FILES = ["site", "nav", "hero", "about", "services", "testimonials", "contact"]

context = {}
for name in DATA_FILES:
    path = DATA / f"{name}.yml"
    if path.exists():
        with open(path) as f:
            context[name] = yaml.safe_load(f)

env = Environment(loader=FileSystemLoader(TEMPLATES))
template = env.get_template("index.html")

context["current_year"] = datetime.now().year

OUTPUT.mkdir(parents=True, exist_ok=True)

html = template.render(**context)
with open(OUTPUT / "index.html", "w") as f:
    f.write(html)

output_images = OUTPUT / "images"
output_images.mkdir(exist_ok=True)
for item in IMAGES.iterdir():
    if item.is_file():
        shutil.copy2(item, output_images / item.name)

print(f"Generated at {OUTPUT / 'index.html'}")
