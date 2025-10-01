#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bedbees.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile

# Activate all users as hosts
for user in User.objects.all():
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.is_host = True
    profile.save()
    print(f"✅ {user.username} is now a HOST")

print("\n🎉 All users are now activated as hosts!")
print("📋 You can now log in with any of these accounts to access the host dashboard:")
for user in User.objects.all()[:5]:
    print(f"   - Username: {user.username}")
