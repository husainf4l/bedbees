# 🚀 Quick Start - BedBees Calendar System

## Prerequisites

✅ Database migrations applied  
✅ Server running on http://127.0.0.1:8000/  
✅ User account with host privileges

---

## 🎯 Quick Test (5 Minutes)

### Step 1: Login as Host

```
1. Go to http://127.0.0.1:8000/signin/
2. Login with host account
3. Navigate to http://127.0.0.1:8000/hostdashboard/
```

### Step 2: Access Calendar

```
1. Click "Calendar & Pricing" in sidebar
2. Select an accommodation from dropdown
3. Calendar should load automatically
```

### Step 3: Edit a Date

```
1. Click any future date (not past dates)
2. Modal opens with edit form
3. Change price (e.g., $150)
4. Toggle availability if needed
5. Click "Save Changes"
6. Calendar refreshes with new data
```

### Step 4: View Public Availability

```
1. Open new tab: http://127.0.0.1:8000/accommodations/
2. Click any accommodation
3. Scroll to "Availability & Pricing" section
4. See real calendar data from host dashboard
```

---

## 🧪 API Testing with curl

### Get Calendar Data

```bash
curl -H "Cookie: sessionid=YOUR_SESSION_ID" \
  "http://127.0.0.1:8000/api/accommodation/1/calendar/?start_date=2025-10-01&end_date=2025-10-31"
```

### Update Single Date

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -d '{
    "date": "2025-10-15",
    "price": 150,
    "is_available": true,
    "minimum_stay": 2
  }' \
  "http://127.0.0.1:8000/api/accommodation/1/calendar/update/"
```

### Bulk Update

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -d '{
    "start_date": "2025-12-24",
    "end_date": "2025-12-31",
    "price": 200,
    "is_special_rate": true,
    "rate_type": "holiday",
    "rate_note": "Christmas Week Special"
  }' \
  "http://127.0.0.1:8000/api/accommodation/1/calendar/bulk-update/"
```

---

## 🎨 What You Should See

### Host Dashboard Calendar

- **Header:** Property selector, stats, action buttons
- **Calendar Grid:** 7 columns (Sun-Sat)
- **Date Cells:** Colored by status
  - Green background = Available
  - Red background = Blocked
  - Blue background = Booked
  - Gray background = Closed
- **Today:** Blue border highlight
- **Prices:** Displayed on each cell
- **Room Count:** "X left" indicator

### Public Listing Page

- **Availability Section:** Grid of date cards
- **Date Cards:** Show date, price, status badge
- **Real-Time:** Updates when you change dates
- **Notice:** "Real-time availability" message

---

## 🔧 Troubleshooting

### Calendar Not Loading

**Check:**

1. JavaScript console for errors (F12)
2. Property is selected in dropdown
3. User is logged in as host
4. Accommodation exists in database

**Fix:**

```javascript
// Open browser console (F12)
window.bedBeesCalendar;
// Should show calendar object
```

### No Properties in Dropdown

**Create a test accommodation:**

```bash
python manage.py shell
```

```python
from core.models import Accommodation, UserProfile
from django.contrib.auth.models import User

# Get host user
user = User.objects.first()
host = user.profile

# Create test accommodation
accommodation = Accommodation.objects.create(
    host=host,
    name="Test Hotel",
    property_type="hotel",
    city="Amman",
    country="Jordan"
)
print(f"Created accommodation ID: {accommodation.id}")
```

### API Returns 403 Forbidden

**Check:**

1. User is logged in
2. User profile has `is_host=True`
3. User owns the accommodation

**Fix:**

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

user = User.objects.first()
user.profile.is_host = True
user.profile.save()
print("User is now a host")
```

### Dates Not Saving

**Check:**

1. Browser console for errors
2. Django server logs: `tail -f server.log`
3. CSRF token in request

**Debug:**

```javascript
// In browser console
fetch("/api/accommodation/1/calendar/update/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    date: "2025-10-20",
    price: 150,
  }),
})
  .then((r) => r.json())
  .then(console.log);
```

---

## 📊 Database Inspection

### View Calendar Data

```bash
python manage.py dbshell
```

```sql
-- View all availability records
SELECT * FROM core_accommodationavailability
ORDER BY date DESC LIMIT 10;

-- Check specific accommodation
SELECT date, price_per_night, is_available, rooms_available
FROM core_accommodationavailability
WHERE accommodation_id = 1
ORDER BY date;

-- View statistics
SELECT
    accommodation_id,
    COUNT(*) as total_dates,
    AVG(price_per_night) as avg_price,
    SUM(CASE WHEN is_available THEN 1 ELSE 0 END) as available_days
FROM core_accommodationavailability
GROUP BY accommodation_id;
```

---

## 🎯 Sample Data Creation

### Create 30 Days of Availability

```bash
python manage.py shell
```

```python
from core.models import Accommodation, AccommodationAvailability
from datetime import date, timedelta
from decimal import Decimal

# Get first accommodation
accommodation = Accommodation.objects.first()

# Create 30 days starting today
start_date = date.today()
for i in range(30):
    current_date = start_date + timedelta(days=i)

    # Weekend pricing
    is_weekend = current_date.weekday() in [4, 5]  # Friday, Saturday
    price = Decimal('150.00') if is_weekend else Decimal('120.00')

    AccommodationAvailability.objects.create(
        accommodation=accommodation,
        date=current_date,
        price_per_night=price,
        is_available=True,
        total_rooms=5,
        rooms_booked=0,
        rooms_blocked=0,
        minimum_stay=2 if is_weekend else 1
    )

print("Created 30 days of availability")
```

---

## ✅ Success Criteria

After following this guide, you should be able to:

- [x] See calendar in host dashboard
- [x] Click and edit dates
- [x] Save changes to database
- [x] See real availability on public listing
- [x] Update prices dynamically
- [x] Block/unblock dates
- [x] View occupancy statistics

---

## 🆘 Getting Help

### Check Logs

```bash
# Django server output
tail -f server.log

# Browser console (F12)
# Look for red error messages
```

### Common Error Messages

**"Property is not defined"**

- Create accommodation first
- Check property selector has options

**"Calendar is not loading"**

- Check JavaScript console
- Verify API endpoints respond
- Check authentication

**"Date not updating"**

- Check CSRF token
- Verify POST request format
- Check user permissions

---

## 📚 Next Steps

1. **Customize Pricing Rules**

   - Add seasonal pricing
   - Create holiday rates
   - Set long-stay discounts

2. **Test Booking Flow**

   - Create test bookings
   - Verify calendar blocks dates
   - Check availability updates

3. **Advanced Features**
   - Bulk edit multiple dates
   - Export to iCal
   - Sync with other platforms

---

**Ready to Go!** 🚀

Your calendar system is fully functional. Start by logging in as a host and exploring the Calendar & Pricing tab!
