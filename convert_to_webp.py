#!/usr/bin/env python3
"""
Convert images to WebP format for better performance
WebP images are 25-35% smaller than JPEG with same quality
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Base directories
BASE_DIR = Path(__file__).resolve().parent
ATTRACTIONS_DIR = BASE_DIR / 'static' / 'core' / 'images' / 'attractions'


def convert_to_webp(image_path, quality=80, keep_original=True):
    """Convert a single image to WebP format"""
    try:
        # Open image
        img = Image.open(image_path)
        
        # Convert RGBA to RGB if necessary (WebP doesn't support RGBA well)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Create output path
        output_path = image_path.with_suffix('.webp')
        
        # Save as WebP
        img.save(output_path, 'WebP', quality=quality, method=6)
        
        # Get file sizes
        original_size = image_path.stat().st_size
        new_size = output_path.stat().st_size
        savings = (1 - new_size / original_size) * 100
        
        print(f"✓ {image_path.name}")
        print(f"  → {output_path.name}")
        print(f"  Original: {original_size/1024:.1f} KB")
        print(f"  WebP: {new_size/1024:.1f} KB")
        print(f"  Saved: {savings:.1f}%\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error converting {image_path.name}: {e}")
        return False


def convert_all(directory=None, quality=80):
    """Convert all JPG and PNG images in directory to WebP"""
    if directory is None:
        directory = ATTRACTIONS_DIR
    
    if not directory.exists():
        print(f"❌ Directory not found: {directory}")
        return
    
    # Find all images
    image_extensions = ['.jpg', '.jpeg', '.png']
    images = []
    for ext in image_extensions:
        images.extend(directory.glob(f'*{ext}'))
        images.extend(directory.glob(f'*{ext.upper()}'))
    
    if not images:
        print("📭 No images found to convert")
        print(f"Looking in: {directory}")
        return
    
    print(f"🔄 Converting {len(images)} images to WebP...")
    print(f"Quality: {quality}%\n")
    
    converted = 0
    for image_path in images:
        # Skip if WebP already exists
        webp_path = image_path.with_suffix('.webp')
        if webp_path.exists():
            print(f"⏭️  Skipping {image_path.name} (WebP already exists)")
            continue
        
        if convert_to_webp(image_path, quality=quality):
            converted += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Converted {converted}/{len(images)} images to WebP")
    
    if converted > 0:
        print(f"\nNext steps:")
        print(f"1. Check the WebP images look good")
        print(f"2. Update image paths in demo_attractions.py")
        print(f"3. Optionally delete original JPG/PNG files")


def show_instructions():
    """Show installation instructions for PIL"""
    print("📦 Pillow (PIL) is required for image conversion")
    print("=" * 60)
    print("\nInstall Pillow:")
    print("  pip install Pillow")
    print("\nOr if using venv:")
    print("  source venv/bin/activate")
    print("  pip install Pillow")
    print("\nThen run this script again:")
    print("  python convert_to_webp.py")


def main():
    """Main entry point"""
    if not PIL_AVAILABLE:
        show_instructions()
        return
    
    print("🖼️  WebP Image Converter")
    print("=" * 60)
    
    # Parse arguments
    quality = 80
    if len(sys.argv) > 1:
        try:
            quality = int(sys.argv[1])
            if not 1 <= quality <= 100:
                print("⚠️  Quality must be between 1-100, using default 80")
                quality = 80
        except ValueError:
            print("⚠️  Invalid quality value, using default 80")
    
    print(f"\nConverting images in: {ATTRACTIONS_DIR}")
    print(f"Quality setting: {quality}% (lower = smaller file, lower quality)\n")
    
    convert_all(ATTRACTIONS_DIR, quality=quality)


if __name__ == '__main__':
    main()
