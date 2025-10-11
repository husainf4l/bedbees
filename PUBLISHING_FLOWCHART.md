# 📊 PUBLISHING SYSTEM - VISUAL FLOWCHART

## 🎯 Complete Publishing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER CREATES NEW LISTING                     │
│                  (Accommodation or Tour Form)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      STEP 6: CHOOSE ACTION                       │
│                                                                  │
│  ┌──────────────────────┐        ┌──────────────────────┐      │
│  │  📋 Save as Draft    │   OR   │  🚀 Publish Now      │      │
│  │  (Gray Button)       │        │  (Green Button)      │      │
│  └──────────┬───────────┘        └──────────┬───────────┘      │
└─────────────┼──────────────────────────────┼──────────────────┘
              │                              │
              │                              │
         DRAFT PATH                    PUBLISH PATH
              │                              │
              ▼                              ▼
┌─────────────────────────┐    ┌─────────────────────────────────┐
│  Status: draft          │    │  1️⃣ NORMALIZE LOCATION          │
│  is_published: False    │    │  Input: "Dubai"                 │
│  is_active: False       │    │  Output: "UAE"                  │
└────────────┬────────────┘    └────────────┬────────────────────┘
             │                              │
             │                              ▼
             │                 ┌─────────────────────────────────┐
             │                 │  2️⃣ VALIDATE & CATEGORIZE       │
             │                 │  City: Dubai                    │
             │                 │  Country: UAE                   │
             │                 │  Type: Villa                    │
             │                 └────────────┬────────────────────┘
             │                              │
             │                              ▼
             │                 ┌─────────────────────────────────┐
             │                 │  3️⃣ PUBLISH LISTING             │
             │                 │  Status: published              │
             │                 │  is_published: True             │
             │                 │  is_active: True                │
             │                 │  published_at: Now              │
             │                 └────────────┬────────────────────┘
             │                              │
             │                              ▼
             │                 ┌─────────────────────────────────┐
             │                 │  4️⃣ SEND EMAILS                 │
             │                 │  ✉️ Host: "Published!"          │
             │                 │  ✉️ Admin: "New listing"        │
             │                 └────────────┬────────────────────┘
             │                              │
             ▼                              ▼
┌─────────────────────────┐    ┌─────────────────────────────────┐
│  SUCCESS MESSAGE        │    │  SUCCESS MESSAGE                │
│  "✅ Saved as draft"    │    │  "🎉 Now LIVE and published!"   │
│  "Publish when ready"   │    │  "Visible in Dubai, UAE"        │
└────────────┬────────────┘    │  "Appears on: Homepage,         │
             │                 │   UAE page, Villa category"      │
             │                 │  "📧 Email sent!"                │
             │                 └────────────┬────────────────────┘
             │                              │
             └──────────────┬───────────────┘
                            │
                            ▼
              ┌──────────────────────────────┐
              │   REDIRECT TO MY LISTINGS    │
              └──────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        MY LISTINGS PAGE                          │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Luxury Villa Dubai              ✅ Published            │  │
│  │  Dubai, UAE • Villa • $500/night                         │  │
│  │  [🔴 Unpublish] [✏️ Edit] [🗑️ Delete]                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Cozy Apartment                  📝 Draft                │  │
│  │  Amman, Jordan • Apartment • $150/night                  │  │
│  │  [🚀 Publish Now] [✏️ Edit] [🗑️ Delete]                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Status Change Flows

### Draft → Published

```
┌─────────────────┐
│  📝 Draft       │
│  (Private)      │
└────────┬────────┘
         │
         │ Click "Publish Now"
         ▼
┌─────────────────┐
│  ⚙️ Processing  │
│  - Normalize    │
│  - Categorize   │
│  - Send Emails  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ✅ Published   │
│  (Live)         │
└─────────────────┘
```

### Published → Draft

```
┌─────────────────┐
│  ✅ Published   │
│  (Live)         │
└────────┬────────┘
         │
         │ Click "Unpublish"
         ▼
┌─────────────────┐
│  📝 Draft       │
│  (Private)      │
└─────────────────┘
```

---

## 🌍 Location Normalization Flow

```
┌──────────────────────────────────────────────────────────┐
│              USER ENTERS LOCATION                        │
│                                                           │
│  Examples:                                               │
│  • "Dubai"                                               │
│  • "dubai"                                               │
│  • "DUBAI"                                               │
│  • "Dubai, UAE"                                          │
│  • "Abu Dhabi"                                           │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│         normalize_location() FUNCTION                    │
│                                                           │
│  1. Convert to lowercase                                 │
│     "Dubai, UAE" → "dubai, uae"                          │
│                                                           │
│  2. Split by comma                                       │
│     ["dubai", "uae"]                                     │
│                                                           │
│  3. Check each part in COUNTRY_MAPPING                   │
│     "dubai" → Found! → "UAE"                             │
│                                                           │
│  4. Return standardized country                          │
│     Result: "UAE"                                        │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│            SAVE TO DATABASE                              │
│            country = "UAE"                               │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│         LISTING APPEARS ON PAGES                         │
│                                                           │
│  • Homepage: /                                           │
│  • Country: /uae/                                        │
│  • Category: /villas/                                    │
└──────────────────────────────────────────────────────────┘
```

---

## 📧 Email Notification Flow

```
┌────────────────────────────────────────────────────────┐
│         LISTING PUBLISHED                              │
└───────────────────────┬────────────────────────────────┘
                        │
                        ├──────────────────┐
                        │                  │
                        ▼                  ▼
        ┌───────────────────────┐  ┌──────────────────────┐
        │   send_listing_       │  │  send_admin_         │
        │   published_email()   │  │  notification()      │
        └──────────┬────────────┘  └──────────┬───────────┘
                   │                          │
                   ▼                          ▼
        ┌───────────────────────┐  ┌──────────────────────┐
        │   TO: Host Email      │  │  TO: admin@bedbees   │
        │                       │  │      .com            │
        │  Subject:             │  │                      │
        │  "Your Listing is     │  │  Subject:            │
        │   Now Live!"          │  │  "New Listing        │
        │                       │  │   Published"         │
        │  Content:             │  │                      │
        │  • Congratulations    │  │  Content:            │
        │  • Property name      │  │  • Property name     │
        │  • Location           │  │  • Type              │
        │  • Category           │  │  • Location          │
        │  • Management link    │  │  • Host              │
        │                       │  │  • Price             │
        └───────────────────────┘  │  • Timestamp         │
                                   │  • Review link       │
                                   └──────────────────────┘
```

---

## 🎨 UI Component Structure

### Create Listing Form (Step 6)

```
┌──────────────────────────────────────────────────────────┐
│                      STEP 6                              │
│                  Review & Publish                        │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  [Property Preview]                                      │
│  • Name: Luxury Villa Dubai                              │
│  • Location: Dubai, UAE                                  │
│  • Type: Villa                                           │
│  • Price: $500/night                                     │
│  • Photos: 5 uploaded                                    │
│                                                           │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Choose Action:                                          │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │  📋 Save as Draft                                  │ │
│  │  Keep this listing private. You can edit and      │ │
│  │  publish it later from "My Listings".              │ │
│  └────────────────────────────────────────────────────┘ │
│            ↑ Gray button, gentle action                  │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │  🚀 Publish Now                                    │ │
│  │  Make this listing live and visible to guests.     │ │
│  │  It will appear on your country and category pages.│ │
│  └────────────────────────────────────────────────────┘ │
│            ↑ Green gradient, prominent action            │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### My Listings Dashboard

```
┌──────────────────────────────────────────────────────────────┐
│                      MY LISTINGS                             │
│  Manage all your accommodation and tour listings             │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Luxury Villa Dubai                   ✅ Published     │ │
│  │  Dubai, UAE • Villa • $500/night                       │ │
│  │  Views: 1,234 • Bookings: 12                           │ │
│  │                                                         │ │
│  │  [🔴 Unpublish]  [✏️ Edit]  [📊 Analytics]  [🗑️ Delete]│ │
│  └────────────────────────────────────────────────────────┘ │
│        ↑ Red: Remove from public view                        │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Cozy Apartment                       📝 Draft         │ │
│  │  Amman, Jordan • Apartment • $150/night                │ │
│  │  Not published yet                                      │ │
│  │                                                         │ │
│  │  [🚀 Publish Now]  [✏️ Edit]  [🗑️ Delete]             │ │
│  └────────────────────────────────────────────────────────┘ │
│        ↑ Green: Make it live                                 │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Beach Resort                         ⏳ Pending       │ │
│  │  Aqaba, Jordan • Resort • $300/night                   │ │
│  │  Waiting for admin approval                             │ │
│  │                                                         │ │
│  │  [✏️ Edit]  [🗑️ Delete]                               │ │
│  └────────────────────────────────────────────────────────┘ │
│        ↑ Orange: Under review (if moderation enabled)        │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Database Schema Flow

```
ACCOMMODATION/TOUR MODEL
┌──────────────────────────────────────┐
│  Fields Used in Publishing:          │
├──────────────────────────────────────┤
│  • country (CharField)               │ ← Normalized by system
│    Example: "UAE"                    │
│                                      │
│  • city (CharField)                  │
│    Example: "Dubai"                  │
│                                      │
│  • property_type/tour_category       │ ← Used for categorization
│    Example: "villa"                  │
│                                      │
│  • status (CharField)                │ ← draft/published/pending
│    Choices:                          │
│    - "draft"                         │
│    - "published"                     │
│    - "pending"                       │
│    - "rejected"                      │
│                                      │
│  • is_published (BooleanField)       │ ← Quick filter
│    True = Live                       │
│    False = Hidden                    │
│                                      │
│  • is_active (BooleanField)          │ ← Additional control
│    True = Enabled                    │
│    False = Disabled                  │
│                                      │
│  • published_at (DateTimeField)      │ ← Timestamp
│    Auto-set on publish               │
│                                      │
│  • host (ForeignKey to User)         │ ← Owner
│                                      │
└──────────────────────────────────────┘
```

---

## 🔐 Optional Moderation Flow

```
MODERATION_ENABLED = False (Default)
┌────────────────────────────────────────────────────────┐
│  User publishes → Status: "published" → Instant live   │
└────────────────────────────────────────────────────────┘

MODERATION_ENABLED = True
┌────────────────────────────────────────────────────────┐
│                                                         │
│  User publishes                                        │
│      ↓                                                  │
│  Status: "pending"                                     │
│      ↓                                                  │
│  Email to admin                                        │
│      ↓                                                  │
│  Admin reviews                                         │
│      ↓                                                  │
│  ┌──────────────┐            ┌──────────────────┐    │
│  │  APPROVE     │     OR     │  REJECT          │    │
│  └──────┬───────┘            └────────┬─────────┘    │
│         │                             │               │
│         ▼                             ▼               │
│  Status: "published"         Status: "rejected"      │
│  Email: "Approved!"          Email: "Needs updates"  │
│  Goes live                   Stays hidden            │
│                                                         │
└────────────────────────────────────────────────────────┘
```

---

## 📱 Mobile-Responsive Design

```
DESKTOP VIEW
┌─────────────────────────────────────────────────────┐
│  [📋 Save as Draft]    [🚀 Publish Now]            │
└─────────────────────────────────────────────────────┘

MOBILE VIEW
┌──────────────────────────┐
│  [📋 Save as Draft]      │
│                          │
│  [🚀 Publish Now]        │
└──────────────────────────┘
```

---

## 🎯 Success Indicators

### After Publishing

```
┌──────────────────────────────────────────────────────────┐
│  ✅ SUCCESS!                                             │
├──────────────────────────────────────────────────────────┤
│  🎉 "Luxury Villa Dubai" is now LIVE and published!     │
│                                                           │
│  ✨ Your property is visible in Dubai, UAE.             │
│                                                           │
│  📍 It appears on:                                       │
│     • Homepage (featured/recent section)                 │
│     • UAE country page (/uae/)                           │
│     • Villa category page (/villas/)                     │
│                                                           │
│  📧 Confirmation email sent to your inbox!               │
│                                                           │
│  [View My Listings]  [Create Another]                    │
└──────────────────────────────────────────────────────────┘
```

---

## 🔍 Where Listings Appear (Visual Map)

```
                    ┌─────────────────────┐
                    │  LISTING PUBLISHED  │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
    ┌────────────────┐ ┌──────────────┐ ┌─────────────────┐
    │   HOMEPAGE     │ │ COUNTRY PAGE │ │ CATEGORY PAGE   │
    │   /            │ │ /uae/        │ │ /villas/        │
    └────────────────┘ └──────────────┘ └─────────────────┘
             │                 │                 │
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  SEARCH RESULTS     │
                    │  (Location-based)   │
                    └─────────────────────┘
```

---

**This visual flowchart shows the complete publishing system at a glance!**

📚 For detailed information:

- Technical docs: `PUBLISHING_SYSTEM_COMPLETE.md`
- User guide: `QUICK_START_PUBLISHING_NEW.md`
- Implementation summary: `IMPLEMENTATION_COMPLETE.md`
