# 🏆 Genius Rewards - Cheat Sheet

## ⚡ Quick Reference Card

---

## 📐 Formulas

### Points Earned

```
Points = (Amount ÷ 50) × 10 × Multiplier
```

### Reward Value

```
Value = (Points ÷ 100) × $10
```

### Examples

| Booking | Level | Multiplier | Points | Value |
| ------- | ----- | ---------- | ------ | ----- |
| $50     | 1     | 1.0x       | 10     | $1    |
| $100    | 1     | 1.0x       | 20     | $2    |
| $150    | 2     | 1.1x       | 33     | $3.30 |
| $200    | 3     | 1.2x       | 48     | $4.80 |
| $500    | 3     | 1.2x       | 120    | $12   |

---

## 🎯 Levels

| Level | Name     | Points  | Discount | Multiplier | Perks     |
| ----- | -------- | ------- | -------- | ---------- | --------- |
| 1     | Explorer | 0-99    | 5%       | 1.0x       | Basic     |
| 2     | Voyager  | 100-299 | 10%      | 1.1x       | +Upgrades |
| 3     | Elite    | 300+    | 15%      | 1.2x       | +VIP      |

---

## 🎁 Rewards (12 Total)

### Level 1 (Everyone)

| Reward         | Points | Value |
| -------------- | ------ | ----- |
| $10 Credit     | 100    | $10   |
| $25 Credit     | 250    | $25   |
| Room Upgrade   | 150    | $50   |
| Early Check-in | 50     | $20   |
| Late Checkout  | 50     | $20   |

### Level 2+ (Voyager & Elite)

| Reward           | Points | Value |
| ---------------- | ------ | ----- |
| $50 Credit       | 500    | $50   |
| Suite Upgrade    | 350    | $150  |
| Weekend Getaway  | 600    | $200  |
| Airport Transfer | 200    | $75   |
| Spa Package      | 400    | $150  |

### Level 3 Only (Elite)

| Reward        | Points | Value |
| ------------- | ------ | ----- |
| Luxury Escape | 1200   | $500  |
| VIP Concierge | 300    | $100  |

---

## 💻 Code Snippets

### Award Points (Automatic)

```python
booking.status = 'completed'
booking.save()  # Points awarded by signal!
```

### Check Points

```python
p = user.genius_profile
print(p.total_points)  # Current points
print(p.reward_value())  # Dollar value
```

### Redeem

```python
reward = Reward.objects.get(id=1)
success, msg = p.redeem_points(reward)
```

---

## 🌐 URLs

| Page      | URL                            |
| --------- | ------------------------------ |
| Dashboard | `/genius-rewards/`             |
| Redeem    | `/genius-rewards/redeem/<id>/` |
| History   | `/genius-rewards/history/`     |
| Bookings  | `/genius-rewards/bookings/`    |
| API       | `/genius-rewards/api/`         |
| Admin     | `/admin/`                      |

---

## 🔧 Commands

```bash
# Test system
python manage.py test_genius_rewards

# Seed rewards
python manage.py seed_rewards

# Migrations
python manage.py makemigrations
python manage.py migrate
```

---

## 📊 Admin Sections

1. **Genius Profiles** - View user stats
2. **Rewards** - Manage rewards
3. **Bookings** - Process bookings
4. **Redemptions** - Fulfill redemptions

---

## ✅ Status Codes

### Booking Status

- `pending` - Not yet complete
- `confirmed` - Confirmed but not done
- `completed` - Done (awards points!)
- `cancelled` - Cancelled

### Redemption Status

- `pending` - Waiting for approval
- `approved` - Approved
- `fulfilled` - Completed
- `cancelled` - Cancelled

---

## 🎯 Quick Tasks

### Add Points Manually

```python
from core.models import GeniusProfile
profile = GeniusProfile.objects.get(user__username='john')
profile.total_points += 100
profile.lifetime_points += 100
profile.save()
profile.update_level()
```

### Create Reward

```python
Reward.objects.create(
    name='Special Offer',
    description='Limited time offer',
    reward_type='special',
    cost_points=200,
    value=50.00,
    min_level=1
)
```

### View User Stats

```python
p = user.genius_profile
print(f"""
Level: {p.level_name}
Points: {p.total_points}
Value: ${p.reward_value()}
Discount: {p.discount_percentage}%
Multiplier: {p.points_multiplier}x
Bookings: {p.total_bookings}
Spent: ${p.total_spent}
""")
```

---

## 🚨 Troubleshooting

| Problem      | Solution                           |
| ------------ | ---------------------------------- |
| No profile   | Run migrations                     |
| No points    | Check booking status = 'completed' |
| No rewards   | Run `seed_rewards`                 |
| Can't redeem | Check points & level               |

---

## 📱 API Response

```json
{
  "success": true,
  "profile": {
    "total_points": 250,
    "level": 2,
    "level_name": "Voyager",
    "discount_percentage": 10,
    "points_multiplier": 1.1,
    "reward_value": 25.00
  },
  "available_rewards": [...]
}
```

---

## ⚡ One-Liners

```python
# Get user level name
user.genius_profile.level_name

# Check if can afford reward
user.genius_profile.total_points >= reward.cost_points

# Get all available rewards for user
Reward.objects.filter(
    is_active=True,
    min_level__lte=user.genius_profile.level
)

# Total value redeemed
user.redemptions.aggregate(Sum('reward__value'))

# Points from last 30 days
Booking.objects.filter(
    user=user,
    status='completed',
    updated_at__gte=timezone.now()-timedelta(days=30)
).aggregate(Sum('points_awarded'))
```

---

## 🎊 That's It!

**Everything you need on one page.**

Print this and keep it handy! 📌
