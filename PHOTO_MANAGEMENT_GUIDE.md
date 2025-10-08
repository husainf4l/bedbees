# 📸 Centralized Photo Management Guide

## Overview

All photos for the BedBees project are stored in a single, organized location for easy management.

## Directory Structure

```
static/core/images/
├── attractions/          # All attraction photos (Petra, Wadi Rum, etc.)
├── countries/           # Country hero images and general photos
├── heroes/              # Large hero/banner images for various pages
├── accommodations/      # Hotel/property photos (already exists)
└── tours/              # Tour-related photos (already exists)
```

## 📁 Main Photo Directory: `static/core/images/attractions/`

This is where **ALL attraction photos** go. Each photo is named with a clear pattern:

### Naming Convention

```
{country}-{attraction-name}-{description}.jpg
```

**Examples:**

- `jordan-petra-treasury.jpg`
- `jordan-petra-monastery.jpg`
- `jordan-petra-royal-tombs.jpg`
- `jordan-wadi-rum-desert.jpg`
- `tunisia-carthage-ruins.jpg`
- `egypt-pyramids-giza.jpg`
- `morocco-marrakech-square.jpg`

### Benefits of This System

✅ All photos in one place - easy to find
✅ Clear naming prevents duplicates
✅ Easy to upload/replace photos
✅ No need for complex folder structures
✅ Works perfectly with your demo_attractions data

---

## 🖼️ Image Format Recommendations

### Recommended Formats (in order of preference):

1. **WebP** (Best choice - modern, smaller file size)

   - 25-35% smaller than JPEG
   - Excellent quality
   - Supported by all modern browsers
   - Example: `jordan-petra-treasury.webp`

2. **JPEG** (Good fallback)

   - Universal support
   - Good compression
   - Example: `jordan-petra-treasury.jpg`

3. **PNG** (For images with transparency only)
   - Use only when you need transparent backgrounds
   - Larger file sizes

### Image Sizes

| Image Type     | Recommended Size | Purpose           |
| -------------- | ---------------- | ----------------- |
| Hero Images    | 1920x1080px      | Main page banners |
| Gallery Photos | 1200x800px       | Photo galleries   |
| Thumbnails     | 600x400px        | Lists, cards      |
| Mobile Hero    | 1080x1920px      | Mobile-optimized  |

### Quality Settings

- **JPEG Quality**: 80-85% (good balance)
- **WebP Quality**: 75-80% (still excellent)
- Keep file sizes under 300KB per image

---

## 📤 How to Upload Photos

### Step 1: Prepare Your Photos

1. **Rename your photos** using the convention:

   ```bash
   jordan-petra-treasury.jpg
   jordan-petra-monastery.jpg
   jordan-wadi-rum-desert.jpg
   ```

2. **Optimize/Resize** (optional but recommended):

   ```bash
   # Using ImageMagick (if installed)
   mogrify -resize 1200x800^ -gravity center -extent 1200x800 -quality 85 *.jpg

   # Or use online tools:
   # - tinypng.com (excellent compression)
   # - squoosh.app (Google's image optimizer)
   # - imageoptim.com (Mac app)
   ```

### Step 2: Upload to Static Directory

**Option A: Direct Copy**

```bash
# Copy all your photos to the attractions folder
cp /path/to/your/photos/*.jpg static/core/images/attractions/
```

**Option B: Using the Upload Script**

```bash
# Use the provided script
python manage_photos.py upload /path/to/your/photos/
```

### Step 3: Update Image References

Photos are automatically available at:

```
/static/core/images/attractions/jordan-petra-treasury.jpg
```

---

## 🔄 Converting Images to WebP (Optional but Recommended)

### Using Python Script (Provided)

```bash
python convert_to_webp.py
```

This will:

- Convert all JPG/PNG in attractions/ to WebP
- Keep originals as backup
- Reduce file sizes by 25-35%

### Using Command Line (if you have ImageMagick)

```bash
cd static/core/images/attractions/
for img in *.jpg; do
    cwebp -q 80 "$img" -o "${img%.jpg}.webp"
done
```

---

## 📋 Current Photo Inventory

### Photos Needed for Major Attractions

#### Jordan

- [x] petra-treasury.jpg (exists)
- [ ] petra-monastery.jpg
- [ ] petra-royal-tombs.jpg
- [ ] petra-siq.jpg
- [ ] petra-great-temple.jpg
- [ ] wadi-rum-desert.jpg
- [ ] dead-sea-shore.jpg
- [ ] jerash-columns.jpg

#### Egypt

- [ ] pyramids-giza.jpg
- [ ] sphinx.jpg
- [ ] luxor-temple.jpg
- [ ] valley-kings.jpg
- [ ] abu-simbel.jpg

#### Morocco

- [ ] marrakech-square.jpg
- [ ] fes-medina.jpg
- [ ] chefchaouen-blue.jpg
- [ ] hassan-tower.jpg
- [ ] casablanca-mosque.jpg

#### Tunisia

- [ ] carthage-ruins.jpg
- [ ] sidi-bou-said.jpg
- [ ] el-jem-amphitheatre.jpg
- [ ] djerba-beach.jpg

#### Algeria

- [ ] algiers-casbah.jpg
- [ ] timgad-ruins.jpg
- [ ] djemila-ruins.jpg
- [ ] constantine-bridge.jpg

---

## 🛠️ Management Scripts

### 1. List All Photos

```bash
python manage_photos.py list
```

### 2. Check Missing Photos

```bash
python manage_photos.py check
```

This will show which attractions are missing photos.

### 3. Generate Thumbnails

```bash
python manage_photos.py thumbnails
```

### 4. Bulk Rename Photos

```bash
python manage_photos.py rename /path/to/photos/ --pattern "jordan-petra"
```

---

## 🔗 Updating demo_attractions.py

When you add new photos, update the image paths in `core/data/demo_attractions.py`:

```python
# OLD (external URL)
'image': 'https://images.unsplash.com/photo-12345...'

# NEW (local file)
'image': '/static/core/images/attractions/jordan-petra-treasury.jpg'

# Or for WebP
'image': '/static/core/images/attractions/jordan-petra-treasury.webp'
```

### Bulk Update Script

```bash
python update_image_paths.py --attraction petra --image-prefix jordan-petra
```

---

## 📊 Photo Quality Checklist

Before uploading photos, ensure:

- [ ] Images are properly named (country-attraction-description)
- [ ] Resolution is appropriate (1200x800 for galleries)
- [ ] File size is under 300KB
- [ ] Images are properly cropped/composed
- [ ] No watermarks (unless required)
- [ ] Images are relevant to the attraction
- [ ] License allows usage (if from external source)

---

## 🚀 Quick Start - Upload Petra Photos

1. **Get your Petra photos ready** (6-8 photos recommended)

2. **Rename them:**

   ```
   jordan-petra-treasury.jpg
   jordan-petra-monastery.jpg
   jordan-petra-royal-tombs.jpg
   jordan-petra-siq.jpg
   jordan-petra-great-temple.jpg
   jordan-petra-high-place.jpg
   ```

3. **Copy to static directory:**

   ```bash
   cp ~/Downloads/petra-photos/*.jpg static/core/images/attractions/
   ```

4. **Update demo_attractions.py:**

   ```bash
   python update_petra_images.py
   ```

5. **Test:**
   ```bash
   # Visit: http://localhost:8000/countries/jordan/attraction/petra/
   ```

---

## 💡 Pro Tips

### Tip 1: Use a Photo Management Tool

- **Adobe Lightroom** - Professional editing
- **Google Photos** - Easy organization
- **Dropbox** - Cloud storage and sharing
- **Figma** - Design and export

### Tip 2: Free Stock Photos (if needed)

- **Unsplash.com** - Free high-quality images
- **Pexels.com** - Free stock photos
- **Pixabay.com** - Free images and videos

### Tip 3: Optimize Before Upload

- Use **TinyPNG.com** to reduce file size
- Use **Squoosh.app** for format conversion
- Keep a backup of original high-res versions

### Tip 4: Consistent Style

- Similar lighting/color grading
- Consistent aspect ratios
- Professional quality only
- Avoid tourist snapshots

---

## 🔒 Photo Attribution

If using stock photos, keep track in `PHOTO_CREDITS.md`:

```markdown
## Petra Photos

- treasury.jpg - Source: Unsplash / Photographer Name
- monastery.jpg - Own photo
- royal-tombs.jpg - Pexels / Photographer Name
```

---

## 📝 Next Steps

1. ✅ Create directory structure (already done)
2. ⏭️ Upload your photos to `static/core/images/attractions/`
3. ⏭️ Run conversion script to create WebP versions
4. ⏭️ Update `demo_attractions.py` with local paths
5. ⏭️ Test pages to ensure photos load correctly
6. ⏭️ Commit and push to git

---

## 🆘 Need Help?

**Photo not showing?**

- Check the path: `/static/core/images/attractions/[filename]`
- Run: `python manage.py collectstatic`
- Clear browser cache (Ctrl+F5)

**File too large?**

- Compress with TinyPNG.com
- Or use the compression script: `python compress_images.py`

**Wrong dimensions?**

- Resize using the script: `python resize_images.py`

---

**Last Updated**: October 8, 2025
