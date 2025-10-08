# 📸 Quick Photo Upload Guide

## ⚡ Fast Setup - 3 Steps

### Step 1: Put ALL photos in ONE folder

```bash
# All your photos go here:
static/core/images/attractions/
```

### Step 2: Name your photos clearly

Use this simple pattern:

```
country-attraction-description.jpg
```

**Examples:**

```
jordan-petra-treasury.jpg
jordan-petra-monastery.jpg
jordan-petra-siq.jpg
jordan-wadi-rum-desert.jpg
egypt-pyramids-giza.jpg
morocco-marrakech-square.jpg
tunisia-carthage-ruins.jpg
```

### Step 3: Copy photos

```bash
# Copy all your photos at once
cp ~/Downloads/my-photos/*.jpg static/core/images/attractions/
```

---

## 🎨 Image Format Guide

### Which format should you use?

**Use JPEG (.jpg)** ✅ RECOMMENDED

- Works everywhere
- Good compression
- Easy to work with
- **This is the simplest choice!**

**Use WebP (.webp)** ⭐ BEST PERFORMANCE

- 30% smaller files
- Faster loading
- Modern format
- Use the converter script: `python convert_to_webp.py`

**Use PNG (.png)** ❌ NOT RECOMMENDED

- Very large files
- Slow loading
- Only use if you need transparency

### Recommended Image Sizes

| Type          | Size      | Example          |
| ------------- | --------- | ---------------- |
| **Hero/Main** | 1920x1080 | Main page banner |
| **Gallery**   | 1200x800  | Photo galleries  |
| **Thumbnail** | 600x400   | List pages       |

**Don't worry too much about size** - the system will handle it!

---

## 🚀 Quick Commands

### Check what photos you have

```bash
python manage_photos.py list
```

### See what's missing

```bash
python manage_photos.py check
```

### Convert to WebP (optional - for better performance)

```bash
# Install Pillow first (one time only)
pip install Pillow

# Convert all images
python convert_to_webp.py
```

---

## 📍 Where Photos Are Used

Your photos appear on:

- Country pages (e.g., `/countries/jordan/`)
- Attraction detail pages (e.g., `/countries/jordan/attraction/petra/`)
- Homepage featured attractions
- Search results
- Gallery views

---

## ✅ Example: Uploading Petra Photos

**1. Get 5-10 photos of Petra**

- From your camera
- From stock photo sites (Unsplash, Pexels)
- From friends/colleagues

**2. Rename them:**

```
jordan-petra-treasury.jpg
jordan-petra-monastery.jpg
jordan-petra-royal-tombs.jpg
jordan-petra-siq.jpg
jordan-petra-great-temple.jpg
```

**3. Copy to folder:**

```bash
cp ~/Downloads/petra/*.jpg static/core/images/attractions/
```

**4. Verify:**

```bash
python manage_photos.py list
```

**5. Test in browser:**

```
http://localhost:8000/countries/jordan/attraction/petra/
```

---

## 🎯 Priority Attractions (Start Here)

### Most Important (Do First)

- ✅ Jordan: Petra, Wadi Rum, Dead Sea
- ✅ Egypt: Pyramids, Sphinx, Luxor
- ✅ Morocco: Marrakech, Fes, Chefchaouen
- ✅ UAE: Burj Khalifa, Sheikh Zayed Mosque

### Important

- Tunisia: Carthage, Sidi Bou Said
- Turkey: Istanbul, Cappadocia
- Algeria: Timgad, Algiers

---

## 🆘 Troubleshooting

**Q: Photos not showing?**

```bash
# Check if file exists
ls -lh static/core/images/attractions/

# Restart Django server
# Press Ctrl+C in terminal, then run:
python manage.py runserver
```

**Q: File too large?**

- Resize to 1200x800 (use any photo editor)
- Or use online tool: tinypng.com

**Q: Wrong format?**

- Just use .jpg - it's the easiest!
- Convert using your photo app or convert_to_webp.py

---

## 📝 Next Steps After Upload

After uploading photos, you need to update the code to use them:

1. **Edit** `core/data/demo_attractions.py`
2. **Find** the attraction (e.g., "petra")
3. **Change** the image URL from:
   ```python
   'image': 'https://images.unsplash.com/...'
   ```
   To:
   ```python
   'image': '/static/core/images/attractions/jordan-petra-treasury.jpg'
   ```

**Or use the bulk update script:**

```bash
# Coming soon: Auto-update script
python update_attraction_images.py
```

---

## 💡 Pro Tips

✅ **Use descriptive filenames** - helps you find photos later
✅ **Keep originals** - store high-res versions elsewhere
✅ **Batch upload** - upload all photos at once, not one by one
✅ **Test regularly** - check pages after uploading
✅ **Optimize** - use WebP for 30% faster loading

---

**Need help?** Run: `python manage_photos.py`
