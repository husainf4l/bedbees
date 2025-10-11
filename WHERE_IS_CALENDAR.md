# ⚠️ IMPORTANT: You're Looking at the Wrong Tab!

## The Problem

You said: "still cant see my Calendar & Pricing in host dashboard under Reservations"

**"Reservations" and "Calendar & Pricing" are TWO DIFFERENT TABS!**

---

## 📍 Where to Find Calendar & Pricing

### Left Sidebar Menu Structure:

```
Host Dashboard
├── 📊 Business Overview
├── 📋 My Listings
├── 📅 Reservations          ← ❌ YOU ARE HERE (WRONG!)
├── 📅 Calendar & Pricing    ← ✅ GO HERE INSTEAD!
├── 💰 Earnings & Payouts
├── 👥 Guest Management
└── ⭐ Reviews & Ratings
```

---

## ✅ Step-by-Step Instructions

### 1. Go to Host Dashboard

```
http://127.0.0.1:8000/hostdashboard/
```

### 2. Look at the LEFT SIDEBAR

You'll see a vertical menu with icons

### 3. Find the FOURTH item

- ❌ NOT "Reservations" (3rd item - shows bookings)
- ✅ Click "Calendar & Pricing" (4th item - manages availability)

### 4. What You Should See

After clicking "Calendar & Pricing":

```
┌─────────────────────────────────────────┐
│ Rates & Availability Calendar            │
│ Booking.com-style calendar with pricing  │
├─────────────────────────────────────────┤
│ Select Property: [The Mayflower Hotel ▾]│
│ Total Rooms: 40 rooms                    │
│ Status: Published & Active               │
├─────────────────────────────────────────┤
│ [Bulk Edit] [Export iCal]               │
├─────────────────────────────────────────┤
│     October 2025                         │
│ S  M  T  W  T  F  S                     │
│          1  2  3  4  5                   │
│ 6  7  8  9 10 11 12                     │
│                                          │
│ (Green cells = Available $100/night)    │
└─────────────────────────────────────────┘
```

---

## 🔍 Still Not Seeing It?

### Debug Step 1: Check Which Tab is Active

1. Open browser Developer Tools (press F12)
2. Go to Console tab
3. Type: `document.getElementById('content-calendar')`
4. Press Enter

**Expected result:** Should show an HTML element
**If null:** The page didn't load correctly

### Debug Step 2: Manually Switch Tab

In the browser console, type:

```javascript
switchTab("calendar");
```

This should force-show the Calendar & Pricing tab.

### Debug Step 3: Check for JavaScript Errors

1. In Console tab, look for any RED error messages
2. Common errors:
   - "switchTab is not defined" → JavaScript didn't load
   - "Failed to fetch" → API issue
   - Network errors → Server not running

### Debug Step 4: Verify User Login

In console, check who you're logged in as:

```javascript
fetch("/api/user/accommodations/")
  .then((r) => r.json())
  .then((d) => console.log("User accommodations:", d));
```

**Expected:** Should show The Mayflower Hotel
**If error 403:** Not logged in as test_host
**If empty array:** No accommodations owned

---

## 🎯 Quick Test

### Test the Tab Switch Directly:

1. **Open browser console** (F12)
2. **Run this command:**

```javascript
// Hide all tabs
document
  .querySelectorAll(".tab-content")
  .forEach((el) => el.classList.add("hidden"));

// Show calendar tab
document.getElementById("content-calendar").classList.remove("hidden");

// Highlight nav item
document.querySelectorAll(".nav-item").forEach((el) => {
  el.classList.remove("text-green-600", "bg-green-50");
  el.classList.add("text-gray-600");
});
document
  .getElementById("nav-calendar")
  .classList.add("text-green-600", "bg-green-50");
```

3. **You should immediately see the calendar!**

---

## 📸 Visual Identification

### How to Tell Them Apart:

#### ❌ Reservations Tab (Wrong)

```
Title: "Reservations"
Subtitle: "Manage guest bookings and reservations"
Content:
  - Table of guest bookings
  - "No reservations yet" message
  - Guest names, check-in/out dates
```

#### ✅ Calendar & Pricing Tab (Correct!)

```
Title: "Rates & Availability Calendar"
Subtitle: "Booking.com-style calendar with per-room pricing"
Content:
  - Property dropdown selector
  - Interactive calendar grid
  - Month navigation arrows
  - Price editing buttons
```

---

## 🚨 Common Mistakes

### Mistake #1: Clicking "Reservations"

- **What it does:** Shows bookings from guests
- **What you need:** Calendar & Pricing (different tab)

### Mistake #2: Looking for Calendar Inside Reservations

- Calendar & Pricing is a **separate top-level tab**
- Not a subtab or section of Reservations

### Mistake #3: Wrong User Account

- Make sure you're logged in as **test_host**
- Not shadishadi, not admin, not any other user

---

## ✅ Verification Checklist

Before asking for help, verify:

- [ ] I'm on `http://127.0.0.1:8000/hostdashboard/`
- [ ] I'm logged in as **test_host** (check top-right corner)
- [ ] I clicked on **"Calendar & Pricing"** (4th item in sidebar)
- [ ] NOT on "Reservations" (3rd item)
- [ ] Browser console shows no JavaScript errors (F12 → Console)
- [ ] Server is running on port 8000

---

## 🎯 Final Answer

**You need to:**

1. Go to hostdashboard
2. Click on **"Calendar & Pricing"** (4th menu item)
3. NOT "Reservations" (3rd menu item)

They are **completely different** tabs!

---

**If you still don't see it after clicking the correct tab, share:**

1. A screenshot of the sidebar menu
2. Browser console errors (F12 → Console tab)
3. Which menu item you clicked on
