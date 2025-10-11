#!/usr/bin/env python3
"""
Download missing high-resolution attraction photos from Unsplash
"""
import os
import requests
from PIL import Image
from io import BytesIO

# Missing photos with alternative Unsplash IDs
missing_photos = {
    "BurjKhalifa5.webp": "photo-1512632578888-169bbbc64f33",
    "grandmosque2.webp": "photo-1512632578888-169bbbc64f33",
    "grandmosque6.webp": "photo-1582672060674-bc2bd808a8b5",
    "PalmJumeirah4.webp": "photo-1512453979798-5ea266f8880c",
}


def download_and_convert_to_webp(photo_id, filename, width=3840, quality=95):
    """Download image from Unsplash and convert to high-quality WebP"""
    url = f"https://images.unsplash.com/{photo_id}?w={width}&q={quality}&fm=jpg"

    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))

        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        output_path = f"static/core/images/{filename}"
        img.save(output_path, "WEBP", quality=quality, method=6)

        file_size = os.path.getsize(output_path) / 1024
        print(f"✓ Saved {filename} ({img.width}x{img.height}, {file_size:.1f}KB)")

    except Exception as e:
        print(f"✗ Error downloading {filename}: {e}")


def main():
    print("Downloading missing photos...\n")

    for idx, (filename, photo_id) in enumerate(missing_photos.items(), 1):
        print(f"[{idx}/{len(missing_photos)}] ", end="")
        download_and_convert_to_webp(photo_id, filename)

    print("\n✓ Done!")


if __name__ == "__main__":
    main()
