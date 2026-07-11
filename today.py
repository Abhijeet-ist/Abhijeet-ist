from pathlib import Path

svg = """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="120">
<rect width="100%" height="100%" fill="#161b22"/>
<text x="20" y="50"
fill="white"
font-size="24"
font-family="monospace">
Hello Abhijeet
</text>
</svg>
"""

Path("dark_mode.svg").write_text(svg)

Path("light_mode.svg").write_text(svg)

print("SVG Generated")