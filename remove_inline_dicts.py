#!/usr/bin/env python3
"""
Remove inline dictionary definitions from views.py
This script removes the countries_data and demo_attractions dictionaries
that are defined inside view functions.
"""

def remove_dict_definition(lines, start_marker, var_name):
    """
    Remove a dictionary definition from the lines.
    
    Args:
        lines: List of lines from the file
        start_marker: String that marks the start of the dict (e.g., "countries_data = {")
        var_name: Variable name being defined
    
    Returns:
        Modified lines list
    """
    result = []
    i = 0
    removed_lines = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is the start of the dictionary definition
        if start_marker in line:
            print(f"Found {var_name} definition at line {i + 1}")
            
            # Count opening and closing braces to find the end
            brace_count = line.count('{') - line.count('}')
            removed_lines = 1
            i += 1
            
            # Skip lines until we find the matching closing brace
            while i < len(lines) and brace_count > 0:
                line = lines[i]
                brace_count += line.count('{') - line.count('}')
                removed_lines += 1
                i += 1
            
            print(f"Removed {removed_lines} lines of {var_name} definition")
            continue
        
        result.append(line)
        i += 1
    
    return result

def main():
    input_file = 'core/views.py'
    output_file = 'core/views.py.new'
    
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Original file: {len(lines)} lines")
    
    # Remove countries_data dictionary
    lines = remove_dict_definition(lines, 'countries_data = {', 'countries_data')
    print(f"After removing countries_data: {len(lines)} lines")
    
    # Remove demo_attractions dictionary
    lines = remove_dict_definition(lines, 'demo_attractions = {', 'demo_attractions')
    print(f"After removing demo_attractions: {len(lines)} lines")
    
    # Write the result
    print(f"\nWriting to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"Done! Created {output_file} with {len(lines)} lines")
    print(f"Removed {13585 - len(lines)} lines total")
    print("\nTo apply changes, run:")
    print(f"  mv {output_file} {input_file}")

if __name__ == '__main__':
    main()
