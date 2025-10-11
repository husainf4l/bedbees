#!/usr/bin/env python3
"""
Image Optimization Script for BedBees
Optimizes all images in static/core/images/ folder to improve site performance
"""

import os
from PIL import Image
import sys

# Configuration
MAX_WIDTH = 1920  # Max width for hero/large images
MAX_HEIGHT = 1080  # Max height for hero/large images
THUMBNAIL_WIDTH = 800  # For smaller images
THUMBNAIL_HEIGHT = 600
WEBP_QUALITY = 85  # Quality for WebP conversion (0-100)
JPEG_QUALITY = 85  # Quality for JPEG optimization

# Image size limits
MAX_FILE_SIZE_MB = 0.5  # Target max 500KB per image


def get_image_size_mb(filepath):
    """Get file size in MB"""
    return os.path.getsize(filepath) / (1024 * 1024)


def optimize_image(
    input_path, max_width=MAX_WIDTH, max_height=MAX_HEIGHT, quality=WEBP_QUALITY
):
    """
    Optimize a single image:
    1. Resize if too large
    2. Convert to WebP
    3. Compress to target quality
    """
    try:
        # Open image
        img = Image.open(input_path)
        original_size = get_image_size_mb(input_path)

        # Convert RGBA to RGB if necessary
        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(
                img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None
            )
            img = background

        # Resize if image is too large
        if img.width > max_width or img.height > max_height:
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

        # Generate output path (convert to .webp)
        base_name = os.path.splitext(input_path)[0]
        output_path = base_name + ".webp"

        # Save as WebP with optimization
        img.save(output_path, "WEBP", quality=quality, method=6)

        new_size = get_image_size_mb(output_path)
        reduction = (
            ((original_size - new_size) / original_size) * 100
            if original_size > 0
            else 0
        )

        print(f"✅ {os.path.basename(input_path)}")
        print(
            f"   {original_size:.2f}MB → {new_size:.2f}MB ({reduction:.1f}% reduction)"
        )
        print(f"   {img.width}x{img.height}px")

        # Remove original if it's not already .webp
        if not input_path.endswith(".webp") and os.path.exists(output_path):
            os.remove(input_path)
            print(f"   🗑️  Removed original {os.path.basename(input_path)}")

        return True, original_size, new_size

    except Exception as e:
        print(f"❌ Error processing {input_path}: {str(e)}")
        return False, 0, 0


def scan_and_optimize(directory):
    """Scan directory and optimize all images"""

    print(f"\n🔍 Scanning: {directory}\n")

    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".webp")
    total_original = 0
    total_optimized = 0
    files_processed = 0
    files_failed = 0

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(image_extensions):
                filepath = os.path.join(root, filename)

                # Check if file is already optimized (< 500KB)
                current_size = get_image_size_mb(filepath)

                if current_size < MAX_FILE_SIZE_MB and filename.endswith(".webp"):
                    print(
                        f"⏭️  Skipping (already optimized): {filename} ({current_size:.2f}MB)"
                    )
                    continue

                # Determine size based on location
                if "hero" in filename.lower() or "banner" in filename.lower():
                    max_w, max_h = MAX_WIDTH, MAX_HEIGHT
                else:
                    max_w, max_h = THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT

                success, orig_size, new_size = optimize_image(
                    filepath, max_width=max_w, max_height=max_h, quality=WEBP_QUALITY
                )

                if success:
                    total_original += orig_size
                    total_optimized += new_size
                    files_processed += 1
                else:
                    files_failed += 1

                print()  # Blank line between files

    # Summary
    print("\n" + "=" * 60)
    print("📊 OPTIMIZATION SUMMARY")
    print("=" * 60)
    print(f"✅ Files processed: {files_processed}")
    print(f"❌ Files failed: {files_failed}")
    print(f"📦 Total before: {total_original:.2f}MB")
    print(f"📦 Total after: {total_optimized:.2f}MB")

    if total_original > 0:
        total_reduction = ((total_original - total_optimized) / total_original) * 100
        print(
            f"💾 Total saved: {total_original - total_optimized:.2f}MB ({total_reduction:.1f}%)"
        )

    print("=" * 60)
    print("\n✨ Optimization complete!")


def main():
    """Main function"""

    # Check if PIL/Pillow is available
    try:
        from PIL import Image
    except ImportError:
        print("❌ Error: Pillow library not found!")
        print("Install it with: pip install Pillow")
        sys.exit(1)

    # Default directory
    images_dir = "static/core/images/"

    if not os.path.exists(images_dir):
        print(f"❌ Error: Directory not found: {images_dir}")
        sys.exit(1)

    print("=" * 60)
    print("🖼️  BedBees Image Optimization Tool")
    print("=" * 60)
    print(f"\n📁 Target directory: {images_dir}")
    print(f"🎯 Max dimensions: {MAX_WIDTH}x{MAX_HEIGHT}px (hero images)")
    print(f"🎯 Max dimensions: {THUMBNAIL_WIDTH}x{THUMBNAIL_HEIGHT}px (other images)")
    print(f"📊 Target quality: {WEBP_QUALITY}%")
    print(f"🎯 Target max size: {MAX_FILE_SIZE_MB}MB per file")

    response = input(
        "\n⚠️  This will convert images to WebP and delete originals. Continue? (yes/no): "
    )

    if response.lower() not in ["yes", "y"]:
        print("❌ Cancelled by user")
        sys.exit(0)

    # Create backup info
    print("\n💡 TIP: Make sure you have a backup before proceeding!")
    backup = input("Do you have a backup? (yes/no): ")

    if backup.lower() not in ["yes", "y"]:
        print("❌ Please create a backup first!")
        print("Run: cp -r static/core/images static/core/images_backup")
        sys.exit(0)

    # Run optimization
    scan_and_optimize(images_dir)


if __name__ == "__main__":
    main()
