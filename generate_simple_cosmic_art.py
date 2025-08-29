import os
import json
import requests
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
import math
import random

# GitHub username to fetch contributions for
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')

# Theme colors - cosmic theme with purples, blues and pinks
COLOR_PALETTE = {
    'background': (13, 17, 23),  # Dark space background
    'low': (102, 126, 234),      # Light blue/indigo (667eea)
    'medium': (118, 75, 162),    # Purple (764ba2)
    'high': (240, 147, 251),     # Pink (f093fb)
    'stars': (255, 255, 255),    # White stars
    'grid': (30, 35, 45),        # Dark grid lines
    'text': (255, 255, 255),     # White text
}

# Get GitHub contributions data
def fetch_contributions():
    try:
        # Use a simpler API endpoint
        url = f"https://github-contributions.vercel.app/api/v1/{GITHUB_USERNAME}"
        response = requests.get(url)
        contributions_data = response.json()
        
        # Process data
        result = []
        for day in contributions_data.get('contributions', []):
            count = day.get('count', 0)
            date = day.get('date', '')
            try:
                weekday = datetime.strptime(date, "%Y-%m-%d").weekday()
            except:
                weekday = 0
            result.append({
                'date': date,
                'count': count,
                'weekday': weekday
            })
        
        return result
        
    except Exception as e:
        print(f"Error fetching contributions: {e}")
        # Generate some sample data if API fails
        return generate_sample_data()

def generate_sample_data():
    result = []
    today = datetime.now()
    for i in range(365):
        date = today - timedelta(days=i)
        result.append({
            'date': date.strftime("%Y-%m-%d"),
            'count': random.randint(0, 15),
            'weekday': date.weekday()
        })
    return result

def create_simple_cosmic_art(contributions):
    # Create a canvas
    width, height = 1200, 800
    canvas = Image.new('RGB', (width, height), COLOR_PALETTE['background'])
    draw = ImageDraw.Draw(canvas)
    
    # Draw a starfield background (simple stars)
    for _ in range(1000):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        draw.ellipse((x, y, x+size, y+size), fill=(brightness, brightness, brightness))
    
    # Sort contributions by date
    contributions.sort(key=lambda x: x['date'])
    
    # Get the max count for normalization
    max_count = max(c['count'] for c in contributions) if contributions else 1
    
    # Map contributions to visual elements in a grid pattern
    grid_size = 20
    rows = 7  # One row per day of week
    cols = max(1, min(52, len(contributions) // rows))  # Ensure at least 1 column
    
    cell_width = (width - 100) / cols
    cell_height = (height - 200) / rows
    
    # Draw contributions as squares in a grid
    for i, contrib in enumerate(contributions[-rows*cols:]):
        col = i % cols
        row = i // cols
        
        # Position
        x = 50 + col * cell_width + cell_width/2
        y = 100 + row * cell_height + cell_height/2
        
        # Size based on contributions
        size_factor = contrib['count'] / max_count if max_count > 0 else 0
        size = 10 + size_factor * 30
        
        # Color based on contribution count
        if size_factor == 0:
            color = COLOR_PALETTE['background']
        elif size_factor < 0.3:
            color = COLOR_PALETTE['low']
        elif size_factor < 0.7:
            color = COLOR_PALETTE['medium']
        else:
            color = COLOR_PALETTE['high']
        
        # Shape based on weekday
        shape_type = contrib['weekday'] % 4
        
        # Draw the shape
        if shape_type == 0:  # Circle
            draw.ellipse((x-size/2, y-size/2, x+size/2, y+size/2), fill=color)
        elif shape_type == 1:  # Square
            draw.rectangle((x-size/2, y-size/2, x+size/2, y+size/2), fill=color)
        elif shape_type == 2:  # Diamond
            draw.polygon([(x, y-size/2), (x+size/2, y), (x, y+size/2), (x-size/2, y)], fill=color)
        else:  # Triangle
            draw.polygon([(x, y-size/2), (x+size/2, y+size/2), (x-size/2, y+size/2)], fill=color)
    
    # Add title
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    title = f"{GITHUB_USERNAME}'s Contribution Galaxy"
    text_width = draw.textlength(title, font=font)
    draw.text((width/2 - text_width/2, 30), title, fill=COLOR_PALETTE['text'], font=font)
    
    return canvas

def main():
    # Get the GitHub username
    if not GITHUB_USERNAME:
        print("GITHUB_USERNAME environment variable not set")
        return
        
    print(f"Generating cosmic art for {GITHUB_USERNAME}...")
    
    # Fetch the contribution data
    contributions = fetch_contributions()
    
    # Create the cosmic art
    cosmic_art = create_simple_cosmic_art(contributions)
    
    # Save the image
    output_dir = "dist"
    os.makedirs(output_dir, exist_ok=True)
    
    cosmic_art.save(f"{output_dir}/cosmic-contribution-art.png")
    print(f"Cosmic contribution art saved to {output_dir}/cosmic-contribution-art.png")

if __name__ == "__main__":
    main()
