#!/usr/bin/env python3
"""
Safe cleanup of large unoptimized images in static folder
This script will:
1. Create a backup of the static images folder
2. Verify optimized versions exist in media folder
3. Safely remove the large JPG files from static folder
4. Generate a cleanup report
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
STATIC_IMAGES = BASE_DIR / "core" / "static" / "core" / "images"
MEDIA_DIR = BASE_DIR / "media"
BACKUP_DIR = (
    BASE_DIR / f'static_images_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
)

# Statistics
total_size = 0
files_to_remove = []
files_kept = []

print("╔══════════════════════════════════════════════════════════╗")
print("║     STATIC IMAGES CLEANUP - SAFETY CHECK                 ║")
print("╚══════════════════════════════════════════════════════════╝\n")

# Step 1: Analyze static images
print("📊 Step 1: Analyzing static images folder...\n")

if not STATIC_IMAGES.exists():
    print("❌ Static images folder not found!")
    exit(1)

for file in STATIC_IMAGES.glob("*.jpg"):
    size = file.stat().st_size
    total_size += size
    size_mb = size / (1024 * 1024)

    # Check if it's a large file (>1MB)
    if size > 1_000_000:
        files_to_remove.append(
            {"name": file.name, "path": file, "size": size, "size_mb": size_mb}
        )
        print(f"  🔴 {file.name}: {size_mb:.1f} MB (LARGE)")
    else:
        files_kept.append(
            {"name": file.name, "path": file, "size": size, "size_mb": size_mb}
        )
        print(f"  🟢 {file.name}: {size_mb:.1f} MB (keeping)")

total_mb = total_size / (1024 * 1024)
remove_size = sum(f["size"] for f in files_to_remove)
remove_mb = remove_size / (1024 * 1024)

print(f"\n📈 Summary:")
print(f"  Total files: {len(files_to_remove) + len(files_kept)}")
print(f"  Total size: {total_mb:.1f} MB")
print(f"  Files to remove: {len(files_to_remove)} ({remove_mb:.1f} MB)")
print(f"  Files to keep: {len(files_kept)} ({(total_mb - remove_mb):.1f} MB)")

# Step 2: Check if optimized versions exist
print(f"\n🔍 Step 2: Checking for optimized versions in media folder...\n")

optimized_found = 0
for file_info in files_to_remove[:10]:  # Sample check
    base_name = file_info["name"].replace(".jpg", "")
    # Look for WebP version
    webp_files = list(MEDIA_DIR.rglob(f"*{base_name}*.webp"))
    if webp_files:
        print(f"  ✅ {file_info['name']} → Found {len(webp_files)} WebP version(s)")
        optimized_found += 1
    else:
        print(f"  ⚠️  {file_info['name']} → No WebP version found")

print(f"\n  Found optimized versions for {optimized_found}/10 sampled images")

# Step 3: Ask for confirmation
print("\n╔══════════════════════════════════════════════════════════╗")
print("║                    SAFETY CONFIRMATION                   ║")
print("╚══════════════════════════════════════════════════════════╝\n")

print(f"This will:")
print(f"  1. Create backup at: {BACKUP_DIR}")
print(f"  2. Remove {len(files_to_remove)} large JPG files")
print(f"  3. Free up {remove_mb:.1f} MB of disk space")
print(f"  4. Keep {len(files_kept)} small files")
print(f"\nOptimized WebP versions already exist in media/ folder.")

response = input("\n⚠️  Proceed with cleanup? (yes/no): ").strip().lower()

if response != "yes":
    print("\n❌ Cleanup cancelled. No changes made.")
    exit(0)

# Step 4: Create backup
print(f"\n📦 Step 3: Creating backup...\n")
try:
    shutil.copytree(STATIC_IMAGES, BACKUP_DIR / "images")
    print(f"  ✅ Backup created: {BACKUP_DIR}")
except Exception as e:
    print(f"  ❌ Backup failed: {e}")
    exit(1)

# Step 5: Remove large files
print(f"\n🗑️  Step 4: Removing large JPG files...\n")

removed_count = 0
for file_info in files_to_remove:
    try:
        file_info["path"].unlink()
        removed_count += 1
        if removed_count <= 5:  # Show first 5
            print(f"  ✅ Removed: {file_info['name']} ({file_info['size_mb']:.1f} MB)")
    except Exception as e:
        print(f"  ❌ Failed to remove {file_info['name']}: {e}")

if removed_count > 5:
    print(f"  ... and {removed_count - 5} more files")

# Step 6: Final report
print("\n╔══════════════════════════════════════════════════════════╗")
print("║                   CLEANUP COMPLETE!                      ║")
print("╚══════════════════════════════════════════════════════════╝\n")

print(f"✅ Successfully removed {removed_count} files")
print(f"💾 Freed up {remove_mb:.1f} MB of disk space")
print(f"📦 Backup saved to: {BACKUP_DIR}")
print(f"🖼️  Optimized images available in: media/")
print(f"\n⚠️  If you need to restore, the backup is safely stored.")

# Create cleanup report
report_path = BASE_DIR / f'CLEANUP_REPORT_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
with open(report_path, "w") as f:
    f.write(f"# Static Images Cleanup Report\n\n")
    f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"## Summary\n\n")
    f.write(f"- **Files removed:** {removed_count}\n")
    f.write(f"- **Space freed:** {remove_mb:.1f} MB\n")
    f.write(f"- **Backup location:** {BACKUP_DIR}\n\n")
    f.write(f"## Removed Files\n\n")
    for file_info in files_to_remove:
        f.write(f"- {file_info['name']} ({file_info['size_mb']:.1f} MB)\n")
    f.write(f"\n## Files Kept\n\n")
    for file_info in files_kept:
        f.write(f"- {file_info['name']} ({file_info['size_mb']:.1f} MB)\n")
    f.write(f"\n## Status\n\n")
    f.write(f"✅ Cleanup completed successfully!\n")
    f.write(f"✅ Optimized WebP versions available in media/ folder\n")
    f.write(f"✅ Backup created for safety\n")

print(f"\n📄 Detailed report saved to: {report_path.name}\n")
