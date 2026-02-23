#!/usr/bin/env python3
# ⒸAngelaMos | 2025 | CertGames.com

import sys
import json
from pathlib import Path

def format_number(num):
    """
    Format number with commas
    """
    return f"{num:,}"

def generate_svg(loc_data):
    """
    Generate SVG card with LOC stats
    """
    total_code = int(loc_data.get('Total', {}).get('code', 0))
    total_lines = int(loc_data.get('Total', {}).get('lines', 0))

    # Count total files - try multiple methods
    total_files = 0
    languages = {}

    # Method 1: Try to get from Total stats (most reliable)
    if 'Total' in loc_data and isinstance(loc_data['Total'], dict):
        total_files = int(loc_data['Total'].get('files', 0))

    # Method 2: If that's 0, count from individual language reports
    if total_files == 0:
        for lang, stats in loc_data.items():
            if lang != 'Total' and isinstance(stats, dict):
                reports = stats.get('reports', [])
                if reports:
                    total_files += len(reports)

    # Second pass: aggregate language stats and merge variants
    for lang, stats in loc_data.items():
        if lang != 'Total' and isinstance(stats, dict):
            code_lines = int(stats.get('code', 0))

            if code_lines > 0:
                # Combine TSX with TypeScript, JSX with JavaScript
                if lang == 'TSX':
                    lang = 'TypeScript'
                elif lang == 'JSX':
                    lang = 'JavaScript'

                # Merge counts if language already exists
                if lang in languages:
                    languages[lang]['code'] += code_lines
                else:
                    languages[lang] = {'code': code_lines}

    # Sort by code count and get top 6
    top_languages = sorted(languages.items(), key=lambda x: x[1]['code'], reverse=True)[:6]

    # Tokyo Night theme palette
    TN_BG         = '#1a1b27'   # card background
    TN_BG_PANEL   = '#24283b'   # bar track / divider panel
    TN_BORDER     = '#292e42'   # subtle border / divider
    TN_FG         = '#c0caf5'   # primary text
    TN_FG_MUTED   = '#565f89'   # secondary / muted text
    TN_PURPLE     = '#bb9af7'   # accent (title, gradient start)
    TN_BLUE       = '#7aa2f7'   # gradient end / fallback bar color
    TN_CYAN       = '#2ac3de'   # "updated" footer text
    TN_RED        = '#f7768e'   # JSON
    TN_ORANGE     = '#ff9e64'   # HTML / Rust
    TN_YELLOW     = '#e0af68'   # JavaScript / JSON alt
    TN_GREEN      = '#9ece6a'   # CSS / Shell / Vue
    TN_TEAL       = '#73daca'   # Go / YAML

    language_colors = {
        'Python':     TN_BLUE,
        'JavaScript': TN_YELLOW,
        'TypeScript': TN_BLUE,
        'Rust':       TN_ORANGE,
        'Go':         TN_TEAL,
        'Java':       TN_ORANGE,
        'Ruby':       TN_RED,
        'C':          TN_FG_MUTED,
        'C++':        TN_RED,
        'C#':         TN_GREEN,
        'PHP':        TN_PURPLE,
        'Swift':      TN_ORANGE,
        'Kotlin':     TN_ORANGE,
        'HTML':       TN_ORANGE,
        'CSS':        TN_GREEN,
        'Sass':       TN_RED,
        'SCSS':       TN_RED,
        'Shell':      TN_GREEN,
        'Haskell':    TN_PURPLE,
        'Vue':        TN_TEAL,
        'JSON':       TN_RED,
        'YAML':       TN_PURPLE,
        'Markdown':   TN_FG_MUTED,
        'Dockerfile': TN_CYAN,
    }

    svg_width = 800
    svg_height = 320

    svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="accent-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{TN_PURPLE};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{TN_BLUE};stop-opacity:0.9" />
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="{svg_width}" height="{svg_height}" fill="{TN_BG}" rx="10"/>

  <!-- Top accent bar -->
  <rect x="10" y="10" width="{svg_width - 20}" height="3" fill="url(#accent-gradient)" rx="1.5"/>

  <!-- Total LOC -->
  <text x="40" y="55" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="32" font-weight="700" fill="{TN_FG}">
    {format_number(total_code)}
  </text>
  <text x="40" y="78" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="13" fill="{TN_FG_MUTED}" letter-spacing="1">
    LINES OF CODE
  </text>

  <!-- Total files (top-right) -->
  <text x="{svg_width - 40}" y="55" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="24" font-weight="600" fill="{TN_FG}" text-anchor="end">
    {format_number(total_files)}
  </text>
  <text x="{svg_width - 40}" y="75" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="12" fill="{TN_FG_MUTED}" text-anchor="end" letter-spacing="1">
    FILES
  </text>

  <!-- Divider -->
  <line x1="30" y1="100" x2="{svg_width - 30}" y2="100" stroke="{TN_BORDER}" stroke-width="1"/>

  <!-- Section title -->
  <text x="40" y="130" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="13" font-weight="600" fill="{TN_PURPLE}" letter-spacing="2">
    TOP LANGUAGES
  </text>
'''

    y_offset = 160
    max_bar_width = svg_width - 350
    max_code = top_languages[0][1]['code'] if top_languages else 1

    for idx, (lang, lang_data) in enumerate(top_languages):
        code_lines = lang_data['code']
        color = language_colors.get(lang, TN_BLUE)
        bar_width = (code_lines / max_code) * max_bar_width
        percentage = (code_lines / total_code) * 100

        svg += f'''
  <text x="40" y="{y_offset}" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="13" fill="{TN_FG}">
    {lang}
  </text>
  <rect x="180" y="{y_offset - 12}" width="{max_bar_width}" height="14" fill="{TN_BG_PANEL}" rx="3"/>
  <rect x="180" y="{y_offset - 12}" width="{bar_width}" height="14" fill="{color}" rx="3" opacity="0.85"/>
  <text x="{180 + max_bar_width + 20}" y="{y_offset}" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="12" fill="{TN_FG}">
    {format_number(code_lines)}
  </text>
  <text x="{svg_width - 40}" y="{y_offset}" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="12" fill="{TN_FG_MUTED}" text-anchor="end">
    {percentage:.1f}%
  </text>
'''
        y_offset += 25

    svg += '''
  <text x="{}" y="{}" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="10" fill="{}" text-anchor="end">
    Updated automatically via GitHub Actions
  </text>
</svg>'''.format(svg_width - 20, svg_height - 10, TN_CYAN)

    return svg

def main():
    loc_file = Path('loc-data.json')

    if not loc_file.exists():
        print("Error: loc-data.json not found!", file=sys.stderr)
        sys.exit(1)

    with open(loc_file, 'r') as f:
        loc_data = json.load(f)

    svg_content = generate_svg(loc_data)

    output_path = Path('loc-stats.svg')
    with open(output_path, 'w') as f:
        f.write(svg_content)

    print(f"SVG generated successfully: {output_path}")

if __name__ == '__main__':
    main()