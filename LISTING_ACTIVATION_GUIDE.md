# 📋 Listing Publication & Activation Guide

## ✅ How Listings Appear on Your Site

For a listing (accommodation or tour) to show on the public website, **BOTH** conditions must be met:

### Required Conditions:
1. **`is_published = True`** - The listing must be published (final review complete)
2. **`is_active = True`** - The listing must be active (not paused by host)

### What Each Field Means:

#### `is_published` (Default: False)
- **False**: Listing is in DRAFT mode - only visible to the host in dashboard
- **True**: Listing has been reviewed and is ready to be shown publicly
- **Purpose**: Allows hosts to create/edit listings without immediately making them public

#### `is_active` (Default: True)
- **True**: Listing is available for booking
- **False**: Listing is temporarily paused (e.g., maintenance, seasonal closure)
- **Purpose**: Allows hosts to quickly pause/unpause listings without deleting them

---

## 🔄 The Listing Workflow

### Step 1: Create Listing
```
Status: is_published=False, is_active=True
Visible: ❌ Not on public site (DRAFT)
Location: ✅ Visible in Host Dashboard only
```

### Step 2: Publish Listing
```
Status: is_published=True, is_active=True
Visible: ✅ Shows on public /accommodations/ or /tours/ pages
Location: ✅ Available for guests to book
```

### Step 3: Pause Listing (Optional)
```
Status: is_published=True, is_active=False
Visible: ❌ Hidden from public site (PAUSED)
Location: ✅ Still in Host Dashboard, can be reactivated anytime
```

### Step 4: Reactivate Listing
```
Status: is_published=True, is_active=True
Visible: ✅ Back on public site
```

---

## 🎯 Quick Actions in Host Dashboard

### "My Listings" Tab Features:
- **Activate Selected**: Sets `is_active=True` for selected listings
- **Deactivate Selected**: Sets `is_active=False` for selected listings
- **Delete Selected**: Permanently removes listings from database

### When to Use What:
- **Deactivate**: Temporary pause (property under renovation, tour seasonal)
- **Delete**: Permanently remove (property sold, tour discontinued)
- **Activate**: Resume accepting bookings

---

## 📝 Publishing Your First Listing

### Current Status:
Currently, when you create a listing through the dashboard:
- `is_published` is set to `False` by default
- `is_active` is set to `True` by default
- **Result**: Listing is NOT visible on public site yet

### To Make It Visible:
You need to manually publish it by setting `is_published=True`. This can be done:

1. **Via Django Admin** (if you have admin access):
   - Go to http://localhost:8000/admin/
   - Find your listing
   - Check the "is published" checkbox
   - Save

2. **Via Database** (development only):
   ```python
   from core.models import Accommodation, Tour

   # Publish all accommodations
   Accommodation.objects.all().update(is_published=True)

   # Publish all tours
   Tour.objects.all().update(is_published=True)
   ```

3. **Add a "Publish" button** to the host dashboard (recommended):
   - Add a publish button next to each listing
   - When clicked, sets `is_published=True`
   - This gives hosts control over when to publish

---

## 🌐 Where Listings Appear

### Public Pages (Requires is_published=True AND is_active=True):
- ✅ `/accommodations/` - All active accommodations
- ✅ `/tours/` - All active tours
- ✅ `/tours/<category>/` - Category-filtered tours
- ✅ Search results
- ✅ Homepage featured listings (if implemented)

### Host Dashboard (Always visible to owner):
- ✅ My Listings tab - Shows ALL your listings regardless of status
- ✅ Can see/edit draft, published, active, and inactive listings

---

## 🔧 Database Commands

### Quick Publish Script:
Run this to publish all existing listings:

```bash
python3 manage.py shell
```

Then in the Python shell:
```python
from core.models import Accommodation, Tour

# Publish all accommodations
count = Accommodation.objects.filter(is_published=False).update(is_published=True)
print(f"Published {count} accommodations")

# Publish all tours
count = Tour.objects.filter(is_published=False).update(is_published=True)
print(f"Published {count} tours")

exit()
```

---

## 📊 Summary Table

| is_published | is_active | Visible on Site? | Can Book? | In Dashboard? |
|--------------|-----------|------------------|-----------|---------------|
| False        | True      | ❌ No (Draft)    | ❌ No     | ✅ Yes        |
| False        | False     | ❌ No (Draft)    | ❌ No     | ✅ Yes        |
| True         | True      | ✅ **YES**       | ✅ **YES**| ✅ Yes        |
| True         | False     | ❌ No (Paused)   | ❌ No     | ✅ Yes        |

---

## 🎉 Answer to Your Question

**Q: "If I publish a real listing, will it show on the site or does it need to be activated?"**

**A:** When you create a listing, you need to do **TWO things**:

1. **Publish it** (set `is_published=True`) - Makes it "ready for public"
2. **Keep it Active** (keep `is_active=True`) - Makes it "currently available"

Both must be `True` for the listing to appear on `/accommodations/` or `/tours/` pages.

By default, new listings are:
- ❌ `is_published=False` (NOT public yet)
- ✅ `is_active=True` (Would be active if published)

So you need to **publish** it first!

---

## 🚀 Next Steps

1. Create your listing through the dashboard
2. Use Django admin or run the publish script to set `is_published=True`
3. Your listing will now appear on the public site!
4. Use "Deactivate" button in dashboard to temporarily hide it
5. Use "Activate" button to make it visible again

---

**Last Updated:** 2025-10-01
