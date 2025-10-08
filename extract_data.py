"""
Data extraction script to create standalone data files for database seeding.
This script extracts countries_data and demo_attractions from views.py
and saves them as JSON files for use in seeding.
"""
import json
import re
from pathlib import Path


def extract_dict_from_views(views_path, dict_name):
    """
    Extract a Python dictionary definition from views.py using regex.
    """
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the dictionary definition
    pattern = rf'{dict_name}\s*=\s*\{{'
    match = re.search(pattern, content)
    
    if not match:
        print(f"Could not find {dict_name} in {views_path}")
        return None
    
    start_pos = match.start()
    
    # Find the matching closing brace
    brace_count = 0
    dict_start = None
    dict_end = None
    
    for i, char in enumerate(content[start_pos:], start=start_pos):
        if char == '{':
            if dict_start is None:
                dict_start = i
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                dict_end = i + 1
                break
    
    if dict_end is None:
        print(f"Could not find closing brace for {dict_name}")
        return None
    
    # Extract the dictionary code
    dict_code = content[start_pos:dict_end]
    
    # Extract just the dict literal part
    equals_pos = dict_code.find('=')
    dict_literal = dict_code[equals_pos+1:].strip()
    
    return dict_literal


def main():
    # Path to views.py
    views_path = Path('/home/aqlaan/Desktop/bedbees/core/views.py')
    output_dir = Path('/home/aqlaan/Desktop/bedbees/core/management/data')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract and save countries_data
    print("Extracting countries_data...")
    countries_code = extract_dict_from_views(views_path, 'countries_data')
    if countries_code:
        countries_file = output_dir / 'countries_data.py'
        with open(countries_file, 'w', encoding='utf-8') as f:
            f.write('# Auto-generated from views.py\n')
            f.write('countries_data = ')
            f.write(countries_code)
        print(f"✅ Saved to {countries_file}")
    
    # Extract and save demo_attractions
    print("\nExtracting demo_attractions...")
    attractions_code = extract_dict_from_views(views_path, 'demo_attractions')
    if attractions_code:
        attractions_file = output_dir / 'demo_attractions.py'
        with open(attractions_file, 'w', encoding='utf-8') as f:
            f.write('# Auto-generated from views.py\n')
            f.write('demo_attractions = ')
            f.write(attractions_code)
        print(f"✅ Saved to {attractions_file}")
    
    print("\n✅ Data extraction complete!")
    print(f"\nData files created in: {output_dir}")
    print("\nYou can now use these files for database seeding.")


if __name__ == '__main__':
    main()
