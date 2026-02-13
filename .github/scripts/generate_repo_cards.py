#!/usr/bin/env python3
import os
import sys
import requests
from datetime import datetime

def create_repo_card_svg(repo_data, theme='light'):
    """Generate a simple SVG card for a repository"""
    
    # Theme colors
    if theme == 'dark':
        bg_color = '#0d1117'
        title_color = '#58a6ff'
        text_color = '#c9d1d9'
        icon_color = '#58a6ff'
        border = 'none'
    else:
        bg_color = '#ffffff'
        title_color = '#0969da'
        text_color = '#24292f'
        icon_color = '#0969da'
        border = '1px solid #d0d7de'
    
    name = repo_data.get('name', 'Unknown')
    description = repo_data.get('description', 'No description provided')
    if description and len(description) > 80:
        description = description[:77] + '...'
    
    stars = repo_data.get('stargazers_count', 0)
    forks = repo_data.get('forks_count', 0)
    language = repo_data.get('language', 'Unknown')
    
    svg = f'''<svg width="400" height="120" xmlns="http://www.w3.org/2000/svg">
  <style>
    .repo-card {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; }}
    .title {{ font-size: 16px; font-weight: 600; fill: {title_color}; }}
    .description {{ font-size: 13px; fill: {text_color}; }}
    .stats {{ font-size: 12px; fill: {text_color}; }}
  </style>
  
  <rect width="400" height="120" rx="6" fill="{bg_color}" stroke="{text_color}" stroke-width="1" opacity="0.2"/>
  
  <!-- Title -->
  <text x="15" y="30" class="repo-card title">{name}</text>
  
  <!-- Description -->
  <text x="15" y="55" class="repo-card description">{description}</text>
  
  <!-- Stats -->
  <g class="repo-card stats">
    <!-- Language -->
    <circle cx="15" cy="95" r="6" fill="{icon_color}"/>
    <text x="28" y="100">{language}</text>
    
    <!-- Stars -->
    <text x="120" y="100">⭐ {stars}</text>
    
    <!-- Forks -->
    <text x="200" y="100">🔀 {forks}</text>
  </g>
</svg>'''
    
    return svg

def fetch_repo_data(owner, repo, token):
    """Fetch repository data from GitHub API"""
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    
    url = f'https://api.github.com/repos/{owner}/{repo}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching {owner}/{repo}: {response.status_code}")
        return None

def main():
    token = os.environ.get('GITHUB_TOKEN')
    
    repos = [
        ('meeTeam05', 'datalogger', 'repo1'),
        ('nhat092005', 'smart-home', 'repo2'),
        ('nhat092005', 'build-os', 'repo3'),
        ('nhat092005', 'cadence-vlsi-lab', 'repo4'),
    ]
    
    os.makedirs('profile', exist_ok=True)
    
    for owner, repo, filename in repos:
        print(f"Generating cards for {owner}/{repo}...")
        repo_data = fetch_repo_data(owner, repo, token)
        
        if repo_data:
            # Generate light mode
            light_svg = create_repo_card_svg(repo_data, theme='light')
            with open(f'profile/{filename}-light.svg', 'w', encoding='utf-8') as f:
                f.write(light_svg)
            
            # Generate dark mode
            dark_svg = create_repo_card_svg(repo_data, theme='dark')
            with open(f'profile/{filename}-dark.svg', 'w', encoding='utf-8') as f:
                f.write(dark_svg)
            
            print(f"  ✓ Generated {filename}-light.svg and {filename}-dark.svg")
        else:
            print(f"  ✗ Failed to generate cards for {owner}/{repo}")

if __name__ == '__main__':
    main()
