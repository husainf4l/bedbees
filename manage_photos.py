#!/usr/bin/env python3
"""
Photo Management Tool for BedBees Project
Helps manage, organize, and optimize attraction photos
"""

import os
import sys
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static' / 'core' / 'images'
ATTRACTIONS_DIR = STATIC_DIR / 'attractions'

def list_photos():
    """List all photos in the attractions directory"""
    print("📸 Photos in attractions directory:\n")
    
    if not ATTRACTIONS_DIR.exists():
        print("❌ Attractions directory doesn't exist!")
        print(f"   Create it: mkdir -p {ATTRACTIONS_DIR}")
        return
    
    photos = sorted(ATTRACTIONS_DIR.glob('*'))
    
    if not photos:
        print("📭 No photos found!")
        print(f"\nUpload photos to: {ATTRACTIONS_DIR}")
        return
    
    # Group by country
    by_country = {}
    for photo in photos:
        if photo.is_file():
            country = photo.stem.split('-')[0] if '-' in photo.stem else 'other'
            if country not in by_country:
                by_country[country] = []
            by_country[country].append(photo)
    
    total_size = 0
    for country, files in sorted(by_country.items()):
        print(f"\n🌍 {country.upper()}")
        print("-" * 60)
        for photo in sorted(files):
            size = photo.stat().st_size / 1024  # KB
            total_size += size
            size_str = f"{size:.1f} KB" if size < 1024 else f"{size/1024:.1f} MB"
            print(f"  ✓ {photo.name:<50} {size_str:>10}")
    
    print(f"\n{'='*60}")
    print(f"Total: {len(photos)} photos | {total_size/1024:.1f} MB")


def check_missing():
    """Check which major attractions are missing photos"""
    print("🔍 Checking for missing attraction photos...\n")
    
    # Major attractions that should have photos
    required_photos = {
        'jordan': ['petra', 'wadi-rum', 'dead-sea', 'jerash'],
        'egypt': ['pyramids', 'sphinx', 'luxor', 'valley-kings'],
        'morocco': ['marrakech', 'fes', 'chefchaouen', 'casablanca'],
        'tunisia': ['carthage', 'sidi-bou-said', 'el-jem', 'djerba'],
        'algeria': ['algiers', 'timgad', 'djemila', 'constantine'],
        'uae': ['burj-khalifa', 'sheikh-zayed-mosque', 'dubai-mall'],
        'saudi-arabia': ['mecca', 'medina', 'jeddah', 'riyadh'],
        'turkey': ['istanbul', 'cappadocia', 'ephesus', 'pamukkale'],
    }
    
    existing_photos = set()
    if ATTRACTIONS_DIR.exists():
        for photo in ATTRACTIONS_DIR.glob('*'):
            if photo.is_file():
                existing_photos.add(photo.stem)
    
    missing_count = 0
    for country, attractions in sorted(required_photos.items()):
        country_missing = []
        for attraction in attractions:
            # Check if any photo exists for this attraction
            has_photo = any(attraction in photo for photo in existing_photos)
            if not has_photo:
                country_missing.append(attraction)
        
        if country_missing:
            print(f"🌍 {country.upper()}")
            for attraction in country_missing:
                print(f"  ❌ {attraction}")
                missing_count += 1
            print()
    
    if missing_count == 0:
        print("✅ All major attractions have photos!")
    else:
        print(f"Total missing: {missing_count} attractions")


def show_upload_instructions():
    """Show instructions for uploading photos"""
    print("📤 How to Upload Photos")
    print("=" * 60)
    print(f"\n1. Copy your photos to this directory:")
    print(f"   {ATTRACTIONS_DIR}")
    print(f"\n2. Use this naming convention:")
    print(f"   country-attraction-description.jpg")
    print(f"\n3. Examples:")
    print(f"   jordan-petra-treasury.jpg")
    print(f"   egypt-pyramids-giza.jpg")
    print(f"   morocco-marrakech-square.jpg")
    print(f"\n4. Run this command:")
    print(f"   cp /path/to/your/photos/*.jpg {ATTRACTIONS_DIR}/")
    print(f"\n5. Verify upload:")
    print(f"   python manage_photos.py list")


def get_stats():
    """Get statistics about photos"""
    if not ATTRACTIONS_DIR.exists():
        print("❌ Attractions directory doesn't exist!")
        return
    
    photos = list(ATTRACTIONS_DIR.glob('*.*'))
    
    # Count by extension
    by_ext = {}
    total_size = 0
    
    for photo in photos:
        if photo.is_file():
            ext = photo.suffix.lower()
            size = photo.stat().st_size
            total_size += size
            by_ext[ext] = by_ext.get(ext, 0) + 1
    
    print("📊 Photo Statistics")
    print("=" * 60)
    print(f"\nTotal Photos: {len(photos)}")
    print(f"Total Size: {total_size / 1024 / 1024:.2f} MB")
    print(f"Average Size: {total_size / len(photos) / 1024:.1f} KB" if photos else "N/A")
    
    print(f"\nBy Format:")
    for ext, count in sorted(by_ext.items()):
        print(f"  {ext}: {count} files")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("📸 BedBees Photo Management Tool")
        print("=" * 60)
        print("\nUsage:")
        print("  python manage_photos.py list      - List all photos")
        print("  python manage_photos.py check     - Check missing photos")
        print("  python manage_photos.py upload    - Show upload instructions")
        print("  python manage_photos.py stats     - Show statistics")
        print("\nExamples:")
        print("  python manage_photos.py list")
        print("  python manage_photos.py check")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        list_photos()
    elif command == 'check':
        check_missing()
    elif command == 'upload':
        show_upload_instructions()
    elif command == 'stats':
        get_stats()
    else:
        print(f"❌ Unknown command: {command}")
        print("Use: list, check, upload, or stats")


if __name__ == '__main__':
    main()
