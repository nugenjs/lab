#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "rich",
# ]
# ///

from rich.console import Console
from rich.theme import Theme

python_theme = Theme(
    {
        "pyyellow": "#ffde57",
        "pyblue": "#4584b6",
    }
)

console = Console(theme=python_theme)

console.print("[pyyellow]hello[/pyyellow] [pyblue]world[/pyblue]", style="on #646464")