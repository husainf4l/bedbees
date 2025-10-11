# 🚀 Genius Rewards - Quick Start Guide

## ✅ System Status: FULLY OPERATIONAL

---

## 📋 Quick Summary

The Genius Rewards system is **activated and ready**. Users automatically earn points from bookings and can redeem them for travel credits, upgrades, and special perks.

---

## 🎯 Key Points

### Points Formula

```
Points = (Booking Amount ÷ 50) × 10 × Level Multiplier
```

### Levels

- **Level 1 (Explorer)**: 0-99 pts → 5% off, 1.0x points
- **Level 2 (Voyager)**: 100-299 pts → 10% off, 1.1x points
- **Level 3 (Elite)**: 300+ pts → 15% off, 1.2x points

### Reward Value

```
Value = (Points ÷ 100) × $10
```

Example: 250 points = $25 value

---

## 🏃 Quick Start

### 1. Access Admin Panel

```bash
Visit: http://127.0.0.1:8000/admin/
```

### 2. View User Profiles

- Click "Core" → "Genius Profiles"
- See all users with their points, levels, and stats

### 3. Manage Rewards

- Click "Core" → "Rewards"
- 12 rewards already seeded
- Add/edit/activate rewards as needed

### 4. Process Bookings

- Click "Core" → "Bookings"
- Change status to "completed" to auto-award points

### 5. Handle Redemptions

- Click "Core" → "Redemptions"
- Select redemptions → "Mark as fulfilled"

---

## 🔥 Auto-Magic Features

### ✅ What Happens Automatically

1. **User Registers** → GeniusProfile created
2. **Booking Created** → Tracked in system
3. **Booking Completed** → Points awarded instantly
4. **Points Threshold Reached** → Level upgraded
5. **Reward Redeemed** → Redemption code generated

### No Manual Work Required!

---

## 💻 For Developers

### Create a Booking (Points Award Automatically)

```python
from core.models import Booking

# Create booking
booking = Booking.objects.create(
    user=request.user,
    booking_type='accommodation',
    total_amount=200.00,
    status='pending'
)

# Complete it (points awarded automatically via signal!)
booking.status = 'completed'
booking.save()
# User now has points!
```

### Check User Points

```python
profile = request.user.genius_profile
print(f"Points: {profile.total_points}")
print(f"Level: {profile.level_name}")
print(f"Value: ${profile.reward_value()}")
```

### Manual Redemption

```python
reward = Reward.objects.get(name='$25 Travel Credit')
success, msg = profile.redeem_points(reward)
print(msg)
```

---

## 🌐 URLs

| Page               | URL                            | Login Required |
| ------------------ | ------------------------------ | -------------- |
| Rewards Dashboard  | `/genius-rewards/`             | ✅             |
| Redeem Reward      | `/genius-rewards/redeem/<id>/` | ✅             |
| Redemption History | `/genius-rewards/history/`     | ✅             |
| Booking History    | `/genius-rewards/bookings/`    | ✅             |
| Reward Detail      | `/reward/<id>/`                | ✅             |
| API Endpoint       | `/genius-rewards/api/`         | ✅             |
| Admin Panel        | `/admin/`                      | ✅ Admin       |

---

## 🧪 Testing

### Run System Test

```bash
python manage.py test_genius_rewards
```

This will:

- ✅ Create test user
- ✅ Create test booking
- ✅ Award points automatically
- ✅ Test redemption flow
- ✅ Verify all features

### Manual Test (Admin)

1. Go to `/admin/core/booking/`
2. Click "Add Booking"
3. Select user, set amount, status="pending"
4. Save
5. Edit booking, change status to "completed"
6. Save → Points awarded!
7. Check user's GeniusProfile to see points

---

## 📊 Pre-Seeded Rewards

### Credits

- $10 Credit - 100 pts
- $25 Credit - 250 pts
- $50 Credit - 500 pts _(Level 2+)_

### Upgrades

- Room Upgrade - 150 pts
- Suite Upgrade - 350 pts _(Level 2+)_

### Getaways

- Weekend (2 nights) - 600 pts _(Level 2+)_
- Luxury (3 nights) - 1200 pts _(Level 3 only)_

### Perks

- Early Check-in - 50 pts
- Late Checkout - 50 pts
- Airport Transfer - 200 pts _(Level 2+)_
- Spa Package - 400 pts _(Level 2+)_
- VIP Concierge - 300 pts _(Level 3 only)_

---

## 📈 Example Scenarios

### Scenario 1: New User

```
1. User registers → Level 1, 0 points
2. Books $100 stay → Booking created
3. Completes stay → +20 points (100/50*10*1.0)
4. Books $150 tour → Booking created
5. Completes tour → +30 points (150/50*10*1.0)
6. Total: 50 points, $5 value
```

### Scenario 2: Level Up

```
1. User has 90 points (Level 1)
2. Books $150 stay → +30 points
3. Total: 120 points → AUTO LEVELS UP TO 2!
4. New multiplier: 1.1x
5. Next booking worth 10% more points
```

### Scenario 3: Redemption

```
1. User has 250 points
2. Redeems $10 Credit (100 pts)
3. Remaining: 150 points
4. Receives code: GR1A2B3C4D
5. Uses code at checkout
```

---

## 🎨 Frontend Integration

### Display User Stats

```django
<!-- In your template -->
<div class="genius-profile">
  <h3>Level {{ user.genius_profile.level_name }}</h3>
  <p>{{ user.genius_profile.total_points }} points</p>
  <p>${{ user.genius_profile.reward_value }} value</p>
  <p>{{ user.genius_profile.discount_percentage }}% discount</p>
</div>
```

### List Available Rewards

```django
{% for reward in available_rewards %}
  <div class="reward">
    <h4>{{ reward.name }}</h4>
    <p>{{ reward.cost_points }} points = ${{ reward.value }}</p>
    <a href="{% url 'redeem_reward' reward.id %}">Redeem</a>
  </div>
{% endfor %}
```

### AJAX API Call

```javascript
fetch("/genius-rewards/api/")
  .then((res) => res.json())
  .then((data) => {
    console.log("Points:", data.profile.total_points);
    console.log("Level:", data.profile.level_name);
    console.log("Rewards:", data.available_rewards);
  });
```

---

## ⚙️ Configuration

### Adjust Point Formula

Edit `core/models.py`, `GeniusProfile.add_points()`:

```python
# Current: base_points = (booking.total_amount / 50) * 10
# Change 50 to 100 for harder earning:
base_points = (booking.total_amount / 100) * 10
```

### Change Level Thresholds

Edit `core/models.py`, `GeniusProfile.update_level()`:

```python
# Current thresholds: 100, 300
# Change to: 200, 500
if self.lifetime_points >= 500:
    self.level = 3
elif self.lifetime_points >= 200:
    self.level = 2
```

### Add New Reward

```python
Reward.objects.create(
    name='Custom Reward',
    description='Your custom reward',
    reward_type='special',
    cost_points=300,
    value=100.00,
    min_level=2,
    is_active=True
)
```

---

## 🐛 Troubleshooting

### Profile Not Created?

```bash
# Manually create for existing users
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from core.models import GeniusProfile
>>> for user in User.objects.all():
...     GeniusProfile.objects.get_or_create(user=user)
```

### Points Not Awarded?

- Check booking status is "completed"
- Check signal is loaded (apps.py has ready() method)
- Check booking.points_awarded field
- Look for console output: "✅ Awarded X points..."

### Rewards Not Showing?

```bash
# Re-seed rewards
python manage.py seed_rewards
```

---

## 📞 Support

### Check Status

```bash
python manage.py test_genius_rewards
```

### View Logs

Look for:

```
✅ Awarded X points to username for booking #ID
```

### Database Check

```bash
python manage.py shell
>>> from core.models import GeniusProfile, Reward
>>> GeniusProfile.objects.count()  # Should match user count
>>> Reward.objects.filter(is_active=True).count()  # Should be 12
```

---

## ✅ Checklist

- [x] Models created
- [x] Migrations applied
- [x] Signals registered
- [x] Admin configured
- [x] Views created
- [x] URLs routed
- [x] Rewards seeded
- [x] System tested
- [x] Documentation complete

---

## 🎉 You're Ready!

The Genius Rewards system is **100% operational** and connected to your `/genius-rewards/` page with **live data** for each user.

**Start using it now!**

1. Visit `/admin/` to manage
2. Create bookings and mark them complete
3. Watch points accumulate
4. Test redemptions
5. Enjoy! 🚀
