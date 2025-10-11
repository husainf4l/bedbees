# 🎯 SOLVED: How to Access Calendar & Pricing

## TL;DR - You're Looking in the Wrong Place!

**Problem:** You said you can't find Calendar & Pricing "under Reservations"

**Solution:** Calendar & Pricing is NOT under Reservations. They are **separate menu items**!

---

## 📍 Navigation Menu (In Order)

When you open http://127.0.0.1:8000/hostdashboard/, the left sidebar shows:

```
1. 📊 Business Overview     ← Default landing page
2. 📋 My Listings           ← List of your properties
3. 📅 Reservations          ← ❌ YOU CLICKED THIS (guest bookings)
4. 📅 Calendar & Pricing    ← ✅ YOU NEED THIS (availability & pricing)
5. 💰 Earnings & Payouts    ← Financial info
6. 👥 Guest Management      ← Guest communications
7. ⭐ Reviews & Ratings      ← Guest feedback
```

---

## ✅ EXACT Steps to Access Calendar & Pricing

### Step 1: Open Host Dashboard

```
URL: http://127.0.0.1:8000/hostdashboard/
```

Make sure you're logged in as **test_host**

### Step 2: Find the Left Sidebar

You'll see a vertical menu on the left side of the screen

### Step 3: Count Down to Item #4

1. Business Overview
2. My Listings
3. Reservations ← Skip this!
4. **Calendar & Pricing** ← **CLICK HERE!**

### Step 4: Look for the Calendar Icon

The Calendar & Pricing menu item has:

- 📅 A calendar icon
- Text: "Calendar & Pricing"
- Location: 4th item from the top

### Step 5: Click It!

When you click "Calendar & Pricing", you'll see:

- Title: "Rates & Availability Calendar"
- Subtitle: "Booking.com-style calendar with per-room pricing"
- A dropdown showing "The Mayflower Hotel"
- A monthly calendar grid

---

## 🔴 What You Were Doing Wrong

You were clicking on **"Reservations"** (item #3) and looking for calendar there.

**Reservations tab shows:**

- Guest bookings
- Check-in/check-out dates for guests
- Reservation status (confirmed, pending, cancelled)
- "No reservations yet" message

**Calendar & Pricing tab shows:**

- Monthly calendar grid
- Availability per date (green = available)
- Pricing per date ($100/night)
- Bulk edit tools
- Property selector dropdown

---

## 🧪 Test It Now

### Quick Console Test

1. Press F12 to open Developer Tools
2. Go to Console tab
3. Paste this and press Enter:

```javascript
// This will switch you to the Calendar tab
switchTab("calendar");
alert("You should now see the Calendar & Pricing tab!");
```

If the calendar appears, it means:
✅ The tab exists and works
✅ You just need to click the correct menu item

---

## 📊 What You'll See in Calendar & Pricing

### Top Section:

```
┌──────────────────────────────────────────────┐
│ Select Property: [The Mayflower Hotel ▼]     │
│ Total Rooms: 40 rooms                         │
│ Status: ● Published & Active                  │
│                                                │
│ [Bulk Edit]  [Export iCal]                   │
└──────────────────────────────────────────────┘
```

### Calendar Grid:

```
          October 2025
Mon Tue Wed Thu Fri Sat Sun
          1   2   3   4   5
  6   7   8   9  10  11  12
 13  14  15  16  17  18  19
 20  21  22  23  24  25  26
 27  28  29  30  31

Each cell shows:
- Date number
- Price ($100)
- Availability (green background = available)
```

### When You Click a Date:

```
┌─────────────────────────────────┐
│ Edit Date: October 15, 2025     │
├─────────────────────────────────┤
│ ☑ Available                     │
│ Price: $ [100.00] per night     │
│ Min Stay: [1] nights            │
│ Max Stay: [30] nights           │
│                                  │
│ Special Rate: [ Select... ▼]    │
│                                  │
│ [Cancel]  [Save]               │
└─────────────────────────────────┘
```

---

## 🔍 Still Having Issues?

### Issue #1: "I clicked Calendar & Pricing but nothing happens"

**Check:**

1. Open browser console (F12)
2. Look for red error messages
3. Run: `document.getElementById('content-calendar')`
4. Should show an element, not null

**Fix:**

```javascript
// Force show the calendar
document.getElementById("content-calendar").classList.remove("hidden");
```

### Issue #2: "The dropdown is empty"

**Check:**

1. You're logged in as test_host
2. In console, run:

```javascript
fetch("/api/user/accommodations/")
  .then((r) => r.json())
  .then(console.log);
```

3. Should show: `{success: true, accommodations: [{id: 53, name: "The Mayflower Hotel", ...}]}`

**Fix:** If empty, the accommodation owner is wrong:

```bash
cd /home/aqlaan/Desktop/bedbees
source venv/bin/activate
python manage.py shell -c "
from core.models import Accommodation;
from django.contrib.auth.models import User;
acc = Accommodation.objects.get(id=53);
acc.host = User.objects.get(username='test_host');
acc.save();
print('Owner updated!')
"
```

### Issue #3: "I see the calendar but it's blank"

**Check:** Availability data exists:

```bash
source venv/bin/activate
python initialize_calendar_data.py
```

---

## 📸 Screenshot Comparison

### ❌ Wrong Tab (Reservations):

```
┌─────────────────────────────────────┐
│ Reservations                         │
│ Manage guest bookings and reservations│
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │  No reservations yet            │ │
│ │                                  │ │
│ │  Reservations will appear here  │ │
│ │  once guests start booking.     │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### ✅ Correct Tab (Calendar & Pricing):

```
┌─────────────────────────────────────┐
│ Rates & Availability Calendar        │
│ Booking.com-style calendar with      │
│ per-room pricing control             │
├─────────────────────────────────────┤
│ Property: [The Mayflower Hotel ▼]   │
│                                      │
│     October 2025                     │
│  Mon Tue Wed Thu Fri Sat Sun        │
│  [6] [7] [8] [9] [10] [11] [12]    │
│  $100 $100 $100 $100 $100 $100 $100│
└─────────────────────────────────────┘
```

---

## ✅ Final Checklist

Before saying "it doesn't work", verify:

- [ ] I'm at http://127.0.0.1:8000/hostdashboard/
- [ ] I'm logged in (see username in top-right)
- [ ] Username is **test_host** (not shadishadi or admin)
- [ ] I clicked **"Calendar & Pricing"** (4th menu item)
- [ ] I did NOT click "Reservations" (3rd menu item)
- [ ] Page title says "Rates & Availability Calendar"
- [ ] I see a dropdown with "The Mayflower Hotel"
- [ ] I see a calendar grid for October 2025

If ALL boxes checked = ✅ **It's working!**

If some boxes unchecked = ❌ **You're in the wrong place**

---

## 🎉 Summary

**The Problem:** You were looking under "Reservations" tab
**The Solution:** Click "Calendar & Pricing" tab instead
**They Are:** Two completely separate menu items
**Location:** Calendar & Pricing is the 4th item in the sidebar

**JUST CLICK THE 4TH MENU ITEM!** 🎯
