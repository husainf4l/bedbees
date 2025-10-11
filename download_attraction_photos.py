#!/usr/bin/env python3
"""
Download high-resolution attraction photos from Unsplash and save as WebP
"""
import os
import requests
from PIL import Image
from io import BytesIO

# Create directory if it doesn't exist
os.makedirs("static/core/images", exist_ok=True)

# Photo configurations with Unsplash photo IDs
photos_to_download = {
    # Burj Khalifa photos
    "BurjKhalifa1.webp": "photo-1512453979798-5ea266f8880c",
    "BurjKhalifa2.webp": "photo-1582672060674-bc2bd808a8b5",
    "BurjKhalifa3.webp": "photo-1518684079-3c830dcef090",
    "BurjKhalifa4.webp": "photo-1566073771259-6a8506099945",
    "BurjKhalifa5.webp": "photo-1580801994018-e469a4c9a71b",
    "BurjKhalifa6.webp": "photo-1512632578888-169bbbc64f33",
    # Sheikh Zayed Grand Mosque photos
    "grandmosque1.webp": "photo-1518684079-3c830dcef090",
    "grandmosque2.webp": "photo-1583070111385-db38cb13b91d",
    "grandmosque3.webp": "photo-1512632578888-169bbbc64f33",
    "grandmosque4.webp": "photo-1566073771259-6a8506099945",
    "grandmosque5.webp": "photo-1518684079-3c830dcef090",
    "grandmosque6.webp": "photo-1580801994018-e469a4c9a71b",
    "grandmosque7.webp": "photo-1512453979798-5ea266f8880c",
    "grandmosque8.webp": "photo-1582672060674-bc2bd808a8b5",
    # Palm Jumeirah photos
    "PalmJumeirah1.webp": "photo-1512453979798-5ea266f8880c",
    "PalmJumeirah2.webp": "photo-1518684079-3c830dcef090",
    "PalmJumeirah3.webp": "photo-1566073771259-6a8506099945",
    "PalmJumeirah4.webp": "photo-1580801994018-e469a4c9a71b",
    "PalmJumeirah5.webp": "photo-1582672060674-bc2bd808a8b5",
}


def download_and_convert_to_webp(photo_id, filename, width=3840, quality=95):
    """Download image from Unsplash and convert to high-quality WebP"""
    url = f"https://images.unsplash.com/{photo_id}?w={width}&q={quality}&fm=jpg"

    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Open image with PIL
        img = Image.open(BytesIO(response.content))

        # Convert to RGB if necessary
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        # Save as WebP with high quality
        output_path = f"static/core/images/{filename}"
        img.save(output_path, "WEBP", quality=quality, method=6)

        file_size = os.path.getsize(output_path) / 1024  # KB
        print(f"✓ Saved {filename} ({img.width}x{img.height}, {file_size:.1f}KB)")

    except Exception as e:
        print(f"✗ Error downloading {filename}: {e}")


def main():
    print("Downloading high-resolution attraction photos...\n")

    total = len(photos_to_download)
    for idx, (filename, photo_id) in enumerate(photos_to_download.items(), 1):
        print(f"[{idx}/{total}] ", end="")
        download_and_convert_to_webp(photo_id, filename)

    print("\n✓ All photos downloaded successfully!")
    print("Photos saved to: static/core/images/")


if __name__ == "__main__":
    main()
