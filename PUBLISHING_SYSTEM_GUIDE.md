# 🚀 BedBees Publishing System - Complete Guide

## Overview

The BedBees Publishing System provides a complete, automated solution for hosts to publish their listings (accommodations, tours, rental cars, and taxi services) with automatic location-based placement, category organization, and optional admin approval.

---

## 🎯 Features Implemented

### ✅ 1. **Automatic Publishing**

- Hosts can publish listings with a single click
- Listings become immediately visible on the site (unless moderation is enabled)
- Automatic location detection and categorization

### ✅ 2. **Location-Based Placement**

- Listings automatically appear on their country page
- Smart location detection from city and country fields
- Supports multiple countries and cities

### ✅ 3. **Category Organization**

- Accommodations: Hotels, Villas, Apartments, etc.
- Tours: Cultural, Adventure, Food & Drink, etc.
- Rental Cars: Sedan, SUV, Luxury, etc.

### ✅ 4. **Status Management**

- **Draft**: Initial state, not visible
- **Pending**: Waiting for admin approval
- **Approved**: Admin approved but not yet published
- **Published**: Live and visible to users
- **Rejected**: Needs revision
- **Suspended**: Temporarily hidden

### ✅ 5. **Email Notifications**

- **Publishing Confirmation**: When host publishes a listing
- **Approval Notification**: When admin approves a listing
- **Rejection Notice**: When admin rejects with feedback
- **Edit Pending**: When changes require approval

### ✅ 6. **Optional Admin Moderation**

- Can be enabled/disabled via `MODERATION_ENABLED` setting
- Admin approval workflow
- Rejection with reason functionality

---

## 📁 Files Added/Modified

### New Files Created:

1. **`core/views_publishing.py`**

   - Publishing views for accommodations, tours, rental cars
   - Unpublishing functionality
   - Admin approval/rejection views
   - Location-based listing API

2. **`core/email_utils.py`**

   - Email templates for all notification types
   - HTML and plain text email support
   - Configurable email settings

3. **`PUBLISHING_SYSTEM_GUIDE.md`** (this file)
   - Complete documentation

### Modified Files:

1. **`core/models.py`**

   - Added `status` field to Accommodation, Tour, RentalCar
   - Added `published_at`, `approved_at`, `approved_by` fields
   - Added `rejection_reason`, `requires_approval` fields
   - Added `publish()` and `get_location_display()` methods

2. **`core/urls.py`**
   - Added publishing/unpublishing URLs
   - Added admin approval/rejection URLs
   - Added location-based API endpoint

---

## 🛠️ How to Use

### For Hosts:

#### Publishing a Listing

**Option 1: Direct Form Submission (Automatic)**
When creating a listing through the forms, listings are automatically published if `MODERATION_ENABLED = False` in `views_publishing.py`.

**Option 2: Manual Publishing (Host Dashboard)**
Add publish buttons to your host dashboard. Here's example HTML:

```django
<!-- In hostdashboard.html -->
{% for accommodation in accommodations %}
<div class="listing-card">
    <h3>{{ accommodation.property_name }}</h3>
    <p>{{ accommodation.city }}, {{ accommodation.country }}</p>

    <!-- Status Badge -->
    <span class="badge badge-{{ accommodation.status }}">
        {{ accommodation.get_status_display }}
    </span>

    <!-- Publish Button -->
    {% if not accommodation.is_published or accommodation.status == 'draft' %}
    <form method="POST" action="{% url 'core:publish_accommodation' accommodation.id %}">
        {% csrf_token %}
        <button type="submit" class="btn btn-success">
            🚀 Publish Listing
        </button>
    </form>
    {% endif %}

    <!-- Unpublish Button -->
    {% if accommodation.is_published and accommodation.status == 'published' %}
    <form method="POST" action="{% url 'core:unpublish_accommodation' accommodation.id %}">
        {% csrf_token %}
        <button type="submit" class="btn btn-warning">
            📥 Unpublish
        </button>
    </form>
    {% endif %}
</div>
{% endfor %}
```

#### Tour Publishing

```django
<form method="POST" action="{% url 'core:publish_tour' tour.id %}">
    {% csrf_token %}
    <button type="submit" class="btn btn-success">
        🚀 Publish Tour
    </button>
</form>
```

#### Rental Car Publishing

```django
<form method="POST" action="{% url 'core:publish_rental_car' car.id %}">
    {% csrf_token %}
    <button type="submit" class="btn btn-success">
        🚀 Publish Vehicle
    </button>
</form>
```

---

### For Admins:

#### Enabling Moderation

In `core/views_publishing.py`, change:

```python
MODERATION_ENABLED = True  # Enable admin approval requirement
```

#### Approving Listings

```django
<!-- In admin panel or custom admin dashboard -->
<a href="{% url 'core:admin_approve_accommodation' accommodation.id %}"
   class="btn btn-success">
    ✅ Approve
</a>
```

#### Rejecting Listings

```django
<a href="{% url 'core:admin_reject_accommodation' accommodation.id %}"
   class="btn btn-danger">
    ❌ Reject
</a>
```

When rejecting, a form will appear to provide a rejection reason.

---

## 🔧 Configuration

### Email Settings

In `settings.py`, configure:

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # or your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'BedBees <noreply@bedbees.com>'

# Site URL for emails
SITE_URL = 'https://www.bedbees.com'  # or your domain
```

### Moderation Settings

In `core/views_publishing.py`:

```python
# Enable/Disable moderation
MODERATION_ENABLED = False  # Set to True to require admin approval

# Auto-publish options (if moderation is disabled)
AUTO_PUBLISH_ON_CREATE = True  # Publish immediately when created
```

---

## 📊 Database Fields

### New Fields Added:

#### Accommodation, Tour, RentalCar Models:

| Field               | Type          | Purpose                                          |
| ------------------- | ------------- | ------------------------------------------------ |
| `status`            | CharField     | Current status (draft, pending, published, etc.) |
| `published_at`      | DateTimeField | When listing was published                       |
| `approved_at`       | DateTimeField | When admin approved                              |
| `approved_by`       | ForeignKey    | Which admin approved                             |
| `rejection_reason`  | TextField     | Why listing was rejected                         |
| `requires_approval` | BooleanField  | Whether changes need approval                    |

---

## 🎨 Status Badge CSS (Optional)

Add to your CSS:

```css
.badge-draft {
  background-color: #e5e7eb;
  color: #374151;
}

.badge-pending {
  background-color: #fef3c7;
  color: #92400e;
}

.badge-published {
  background-color: #d1fae5;
  color: #065f46;
}

.badge-rejected {
  background-color: #fee2e2;
  color: #991b1b;
}

.badge-suspended {
  background-color: #fecaca;
  color: #7f1d1d;
}
```

---

## 🔄 Workflow Diagrams

### Publishing Flow (No Moderation):

```
Host Creates Listing
       ↓
Fills Form & Submits
       ↓
Status: "draft"
       ↓
Host Clicks "Publish"
       ↓
Status: "published"
       ↓
Email Sent to Host
       ↓
Listing Visible on Site
```

### Publishing Flow (With Moderation):

```
Host Creates Listing
       ↓
Fills Form & Submits
       ↓
Status: "draft"
       ↓
Host Clicks "Publish"
       ↓
Status: "pending"
       ↓
Email: "Under Review"
       ↓
Admin Reviews
       ↓
    [Approve]              [Reject]
       ↓                      ↓
Status: "published"    Status: "rejected"
       ↓                      ↓
Email: "Approved"      Email: "Needs Changes"
       ↓
Listing Visible on Site
```

---

## 🌍 Location-Based Display

Listings automatically appear on country pages based on their location:

```python
# Views automatically filter by location
accommodations = Accommodation.objects.filter(
    country__iexact=country,
    is_published=True,
    is_active=True,
    status='published'
)
```

### Country Page Template Example:

```django
<!-- In country_detail.html -->
<h2>Accommodations in {{ country }}</h2>

{% for accommodation in accommodations %}
<div class="accommodation-card">
    <h3>{{ accommodation.property_name }}</h3>
    <p>{{ accommodation.city }}, {{ accommodation.country }}</p>
    <p>{{ accommodation.base_price }} / night</p>
    <a href="{% url 'core:accommodation_detail' accommodation.id %}">
        View Details
    </a>
</div>
{% endfor %}
```

---

## 📧 Email Templates

### Publishing Confirmation Email:

- **Subject**: "🎉 Your listing is now live on BedBees!"
- **Content**: Congratulations message with dashboard link
- **When Sent**: Immediately after publishing (if no moderation)

### Approval Email:

- **Subject**: "✅ Your listing has been approved!"
- **Content**: Approval confirmation with go-live date
- **When Sent**: When admin approves listing

### Rejection Email:

- **Subject**: "⚠️ Action required: Your listing needs attention"
- **Content**: Reason for rejection + edit instructions
- **When Sent**: When admin rejects listing

### Edit Pending Email:

- **Subject**: "📝 Your listing update is under review"
- **Content**: Acknowledgment of submitted changes
- **When Sent**: When changes require approval

---

## 🧪 Testing

### Test Publishing:

1. Create a new accommodation
2. Go to host dashboard
3. Click "Publish Listing"
4. Check that:
   - Status changes to "published"
   - Listing appears on homepage
   - Listing appears on country page
   - Email is sent (check console if DEBUG=True)

### Test with Moderation:

1. Set `MODERATION_ENABLED = True`
2. Publish a listing
3. Status should be "pending"
4. Go to admin panel
5. Approve the listing
6. Check listing is now visible

---

## 🚨 Troubleshooting

### Emails Not Sending:

Check your email configuration in `settings.py`:

```bash
# Test email in Django shell
python manage.py shell

from core.email_utils import send_listing_published_email
from core.models import Accommodation

accommodation = Accommodation.objects.first()
send_listing_published_email(accommodation, 'accommodation')
```

### Listings Not Appearing:

Check filters in views:

```python
# Must have all three
is_published=True
is_active=True
status='published'
```

### Status Not Updating:

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🔐 Security Considerations

1. **CSRF Protection**: All forms use `{% csrf_token %}`
2. **User Authentication**: `@login_required` on all publishing views
3. **Ownership Verification**: Views check `host=request.user`
4. **Admin-Only Actions**: `@user_passes_test(is_admin)` on admin views

---

## 🎉 Success Metrics

After implementation, you should see:

- ✅ Hosts can publish with one click
- ✅ Listings auto-categorize by location
- ✅ Email notifications sent successfully
- ✅ Admin approval workflow (if enabled)
- ✅ Listings visible on correct pages
- ✅ Status badges show current state

---

## 📞 Support

If you need help:

1. Check this guide
2. Review code comments in `views_publishing.py`
3. Check Django logs for errors
4. Test email configuration

---

## 🔄 Future Enhancements

Consider adding:

- [ ] Batch publishing (publish multiple listings at once)
- [ ] Scheduled publishing (set future publish date)
- [ ] Preview mode (view before publishing)
- [ ] Analytics dashboard (views, bookings per listing)
- [ ] Auto-expiry (unpublish after X days)
- [ ] Featured listings system
- [ ] Social media sharing on publish

---

**Happy Publishing! 🎊**

_Built with ❤️ for BedBees_
