# 🚀 BedBees Host Dashboard - Quick Reference

## ⚡ Quick Start (3 Steps)

### 1. Start Server

```bash
cd /home/aqlaan/Desktop/bedbees
python manage.py runserver
```

### 2. Open Browser

```
http://localhost:8000/hostdashboard/
```

### 3. Login

- **Username**: `admin`
- **Password**: `admin123`

---

## 📊 Database Status

✅ **16 Countries** with 262 attractions  
✅ **36 Accommodations** (all published)  
✅ **18 Tours** (16 published)  
✅ **35 Listings** with full inventory  
✅ **199 Photos** across all listings  
✅ **1,255 Inventory Records** for 30-day availability

---

## 🛠️ Useful Commands

### Re-seed Everything

```bash
python manage.py seed_all --clear --create-admin
python manage.py seed_demo_data
```

### Check Database Status

```bash
python check_dashboard.py
```

### Verify System

```bash
python manage.py check
```

### Apply Migrations

```bash
python manage.py migrate
```

---

## 🎯 Available URLs

| Page                 | URL                      | Login Required |
| -------------------- | ------------------------ | -------------- |
| Home                 | `/`                      | No             |
| Host Dashboard       | `/hostdashboard/`        | **Yes**        |
| Create Accommodation | `/create_accommodation/` | **Yes**        |
| Create Tour          | `/create_tour/`          | **Yes**        |
| My Profile           | `/host_profile/`         | **Yes**        |
| Django Admin         | `/admin/`                | **Yes**        |

---

## 🔐 Test Accounts

### Admin (Full Access)

- Username: `admin`
- Password: `admin123`
- Role: Superuser + Host
- Verified: ✅ All verifications

### Demo Hosts (5 users)

- Username: `demo_host_1` to `demo_host_5`
- Password: `demo123`
- Role: Host
- Each has sample listings

---

## 🎨 Dashboard Features

### ✅ Working Features

- Dashboard overview with statistics
- My Profile management
- My Listings (view, filter, sort)
- Create new accommodations
- Create new tours
- Bulk operations (activate, deactivate, publish, delete)
- Photo management
- Location mapping
- Availability calendar

### 🚧 To Be Implemented

- Bookings management
- Reviews system
- Earnings tracking
- Messaging system
- Advanced settings

---

## 📱 Key Files

### Templates

- `core/templates/core/hostdashboard.html` - Main dashboard
- `core/templates/core/navbar.html` - Navigation

### Models

- `core/models.py` - All database models

### Views

- `core/views.py` - All view functions

### Data Modules

- `core/data/countries_data.py` - Countries
- `core/data/demo_attractions.py` - Attractions
- `core/data/demo_accommodations.py` - Sample properties

### Management Commands

- `core/management/commands/seed_all.py` - Master seed
- `core/management/commands/seed_demo_data.py` - Demo listings

---

## 🆘 Quick Fixes

### Issue: Can't access dashboard

```bash
# Make sure user is a host
python manage.py shell -c "from core.models import *; u = User.objects.get(username='admin'); p = u.profile; p.is_host = True; p.save()"
```

### Issue: No listings

```bash
python manage.py seed_demo_data
```

### Issue: Missing countries

```bash
python manage.py seed_all --create-admin
```

### Issue: Database errors

```bash
python manage.py migrate
```

---

## 📈 Next Development Steps

1. ✅ ~~Seed all data~~ **COMPLETE**
2. ✅ ~~Fix URL namespacing~~ **COMPLETE**
3. ✅ ~~Clean up UI~~ **COMPLETE**
4. 🚧 Implement bookings system
5. 🚧 Add reviews functionality
6. 🚧 Create messaging system
7. 🚧 Build earnings dashboard
8. 🚧 Add advanced filters

---

## 🎉 Status: READY FOR TESTING

All backend modules seeded ✅  
Host dashboard functional ✅  
Admin user configured ✅  
Demo data populated ✅  
URL routing fixed ✅

**Start now**: `python manage.py runserver`

---

_Quick Reference Guide - Last Updated: October 10, 2025_
