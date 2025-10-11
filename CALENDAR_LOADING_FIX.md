# Calendar Loading Fix - Applied ✅

## Problem

The Calendar & Pricing page was showing but empty - no properties in the dropdown, no calendar grid.

## Root Cause

The JavaScript that loads properties was running on `DOMContentLoaded` (page load), but at that time the Calendar tab was **hidden**. The code tried to populate the dropdown before you clicked on the Calendar tab.

## Solution Applied

### 1. Created `loadCalendarProperties()` Function

New function that:

- Fetches accommodations from `/api/user/accommodations/`
- Populates the dropdown with property names
- Auto-selects the first property
- Loads the calendar for that property
- Includes error handling and console logging

### 2. Trigger on Tab Switch

Modified `switchTab()` function to call `loadCalendarProperties()` when switching to the calendar tab:

```javascript
// Initialize calendar when switching to calendar tab
if (tabName === "calendar") {
  loadCalendarProperties();
}
```

### 3. Added Console Logging

Now logs:

- "Loading calendar properties..."
- API response status
- Number of properties loaded
- Any errors encountered

## Testing Steps

### 1. Reload the Page

```
http://127.0.0.1:8000/hostdashboard/
```

### 2. Open Browser Console

Press **F12** → Go to **Console** tab

### 3. Click "Calendar & Pricing"

You should see console messages:

```
Switching to tab: calendar
Loading calendar properties...
API response status: 200
API data received: {success: true, accommodations: [{...}]}
Loaded 1 properties
```

### 4. Check the Dropdown

The "Select Property" dropdown should now show:

```
[The Mayflower Hotel ▼]
```

### 5. Calendar Should Load

You should see:

- Monthly calendar grid
- Dates showing $100/night
- Green backgrounds for available dates

## If It Still Doesn't Work

### Check Console for Errors

**Error: "API response status: 403"**

- **Cause:** Not logged in or not a host
- **Fix:** Log in as test_host

**Error: "API response status: 401"**

- **Cause:** Not authenticated
- **Fix:** Make sure you're logged in

**Error: "No accommodations found in response"**

- **Cause:** API returned empty array
- **Fix:** Run this to verify ownership:

```bash
cd /home/aqlaan/Desktop/bedbees
source venv/bin/activate
python manage.py shell -c "
from core.models import Accommodation;
from django.contrib.auth.models import User;
user = User.objects.get(username='test_host');
accs = Accommodation.objects.filter(host=user);
print(f'Found {accs.count()} accommodations');
[print(f'  - {a.property_name} (ID: {a.id})') for a in accs];
"
```

**Error: "BedBeesCalendar is not defined"**

- **Cause:** calendar.js didn't load
- **Fix:** Check if `/static/core/js/calendar.js` exists and is accessible

### Manual Test in Console

Open browser console and run:

```javascript
// Test API directly
fetch("/api/user/accommodations/")
  .then((r) => r.json())
  .then((d) => console.log("API Result:", d))
  .catch((e) => console.error("API Error:", e));

// Test property loading function
loadCalendarProperties();
```

### Force Reload Everything

If cache is causing issues:

1. Press **Ctrl+Shift+R** (hard reload)
2. Or press **Ctrl+Shift+Delete** → Clear cache
3. Reload page

## What You Should See Now

### Property Dropdown:

```
┌────────────────────────────────┐
│ Select Property                │
│ [The Mayflower Hotel        ▼] │ ← Should show your property
└────────────────────────────────┘
```

### Calendar Grid:

```
     October 2025
Sun Mon Tue Wed Thu Fri Sat
          1   2   3   4   5
          $100 $100 $100 $100 $100
  6   7   8   9  10  11  12
$100 $100 $100 $100 $100 $100 $100
```

### Total Rooms Display:

```
┌──────────────┐
│ Total Rooms  │
│ 1 room       │ ← Should update based on property
└──────────────┘
```

## Files Modified

- `/home/aqlaan/Desktop/bedbees/core/templates/core/hostdashboard.html`
  - Added `loadCalendarProperties()` function
  - Modified `switchTab()` to call it when tab = 'calendar'
  - Updated DOMContentLoaded event handler

## Status

✅ **FIXED** - Calendar properties now load when you click the tab!

---

**Next:** Click "Calendar & Pricing" and check browser console for any errors.
If you see errors, copy them and share so I can debug further.
