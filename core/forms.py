from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Accommodation, Tour, TourGuide, RentalCar

class HostRegistrationForm(forms.ModelForm):
    """Custom form for host registration"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-2xl focus:ring-4 focus:ring-green-100 focus:border-green-500 transition-all duration-200 hover:border-gray-300 hover:shadow-lg hover:shadow-gray-100/50 bg-white/50 backdrop-blur-sm',
            'placeholder': 'Create a password (min 6 characters)'
        }),
        min_length=6,
        help_text="Password must be at least 6 characters long."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-2xl focus:ring-4 focus:ring-green-100 focus:border-green-500 transition-all duration-200 hover:border-gray-300 hover:shadow-lg hover:shadow-gray-100/50 bg-white/50 backdrop-blur-sm',
            'placeholder': 'Confirm your password'
        })
    )
    terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded-lg hover:border-green-400 transition-colors'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'block w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-2xl focus:ring-4 focus:ring-green-100 focus:border-green-500 transition-all duration-200 hover:border-gray-300 hover:shadow-lg hover:shadow-gray-100/50 bg-white/50 backdrop-blur-sm',
                'placeholder': 'Choose a username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'block w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-2xl focus:ring-4 focus:ring-green-100 focus:border-green-500 transition-all duration-200 hover:border-gray-300 hover:shadow-lg hover:shadow-gray-100/50 bg-white/50 backdrop-blur-sm',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-2xl focus:ring-4 focus:ring-green-100 focus:border-green-500 transition-all duration-200 hover:border-gray-300 hover:shadow-lg hover:shadow-gray-100/50 bg-white/50 backdrop-blur-sm',
                'placeholder': 'Enter your email'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Create UserProfile for host
            UserProfile.objects.create(user=user, is_host=True)
        return user


class HostProfileForm(forms.ModelForm):
    """Form for editing host profile information"""
    
    # User fields
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
            'placeholder': 'Enter your last name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
            'placeholder': 'Enter your email address'
        })
    )

    class Meta:
        model = UserProfile
        fields = [
            'profile_picture', 'phone_number', 'date_of_birth', 'bio',
            'address', 'city', 'country', 'postal_code',
            'host_since', 'languages_spoken',
            'business_name', 'business_logo', 'business_type', 'mission_statement',
            'hosting_approach', 'response_time', 'response_rate', 'special_services',
            'sustainability_practices', 'awards_badges',
            'website', 'instagram', 'facebook', 'twitter',
            'email_notifications', 'sms_notifications', 'marketing_emails',
            # Verification Documents
            'identity_document', 'business_license', 'tax_document',
            'insurance_document', 'banking_document'
        ]
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
                'accept': 'image/*'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'placeholder': '+1 (555) 123-4567'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'type': 'date'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300 resize-none',
                'rows': 4,
                'placeholder': 'Tell guests about yourself, your hosting experience, and what makes your place special...'
            }),
            'address': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'placeholder': '123 Main Street'
            }),
            'city': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'placeholder': 'Enter your city'
            }),
            'country': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'placeholder': 'Enter your country'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'placeholder': '12345'
            }),
            'languages_spoken': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'placeholder': 'English, Spanish, French'
            }),
            'host_since': forms.DateInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'type': 'date'
            }),
            'business_name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'placeholder': 'Your business or property name'
            }),
            'business_logo': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': 'image/*'
            }),
            'business_type': forms.Select(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300'
            }),
            'mission_statement': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300 resize-none',
                'rows': 3,
                'placeholder': 'Your mission or what makes your hosting special (max 300 characters)',
                'maxlength': 300
            }),
            'hosting_approach': forms.Select(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300'
            }),
            'response_time': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'placeholder': 'e.g., Within 1 hour, Within 24 hours'
            }),
            'response_rate': forms.NumberInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'placeholder': 'Response rate % (0-100)',
                'min': 0,
                'max': 100
            }),
            'special_services': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300 resize-none',
                'rows': 4,
                'placeholder': 'e.g., Airport pickup, Guided tours, Local recommendations, 24/7 support'
            }),
            'sustainability_practices': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300 resize-none',
                'rows': 4,
                'placeholder': 'Describe your eco-friendly practices, local community support, etc.'
            }),
            'awards_badges': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300 resize-none',
                'rows': 3,
                'placeholder': 'List any awards, certifications, or special recognitions'
            }),
            'website': forms.URLInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'placeholder': 'https://yourwebsite.com'
            }),
            'instagram': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'placeholder': '@yourusername'
            }),
            'facebook': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'placeholder': 'Facebook page URL or username'
            }),
            'twitter': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 hover:border-gray-300',
                'placeholder': '@yourusername'
            }),
            'email_notifications': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            }),
            'sms_notifications': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            }),
            'marketing_emails': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            }),
            # Verification Documents
            'identity_document': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'business_license': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'tax_document': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-yellow-50 file:text-yellow-700 hover:file:bg-yellow-100',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'insurance_document': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'banking_document': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
        
        # Set notification preferences to True by default
        self.fields['email_notifications'].initial = True
        self.fields['sms_notifications'].initial = True
        self.fields['marketing_emails'].initial = True

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Update user fields
            if self.user:
                self.user.first_name = self.cleaned_data['first_name']
                self.user.last_name = self.cleaned_data['last_name']
                self.user.email = self.cleaned_data['email']
                self.user.save()
            profile.save()
        return profile


class AccommodationForm(forms.ModelForm):
    """Form for creating accommodation listings"""

    class Meta:
        model = Accommodation
        fields = ['host_name', 'entity_type', 'contact_email', 'contact_phone', 'business_address', 'tax_id', 'bank_account', 'property_name', 'property_type', 'star_rating', 'country', 'city', 'street_address', 'latitude', 'longitude', 'num_rooms', 'beds_per_room', 'bed_type', 'num_bathrooms', 'max_guests', 'property_size', 'tagline', 'full_description', 'property_features', 'nearby_landmarks', 'checkin_time', 'checkout_time', 'amenities', 'base_price', 'cleaning_fee', 'extra_guest_fee', 'tax_rate', 'cancellation_policy', 'house_rules']
        widgets = {
            'host_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'entity_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'business_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3
            }),
            'tax_id': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'bank_account': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'property_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'property_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'star_rating': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'street_address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'latitude': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'longitude': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'num_rooms': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'beds_per_room': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'bed_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'num_bathrooms': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'max_guests': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'property_size': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'tagline': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'maxlength': 150
            }),
            'full_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 6
            }),
            'property_features': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 4
            }),
            'nearby_landmarks': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3
            }),
            'checkin_time': forms.TimeInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'time'
            }),
            'checkout_time': forms.TimeInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'time'
            }),
            'amenities': forms.SelectMultiple(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'size': '8'
            }),
            'base_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'step': '0.01'
            }),
            'cleaning_fee': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'step': '0.01'
            }),
            'extra_guest_fee': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'step': '0.01'
            }),
            'tax_rate': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'step': '0.01'
            }),
            'cancellation_policy': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'house_rules': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 4
            }),
        }


class TourForm(forms.ModelForm):
    """Form for creating tour listings"""

    # Country and City choices
    COUNTRY_CHOICES = [
        ('', 'Select Country'),
        ('Jordan', 'Jordan'),
        ('UAE', 'United Arab Emirates'),
        ('Egypt', 'Egypt'),
        ('Lebanon', 'Lebanon'),
        ('Qatar', 'Qatar'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Kuwait', 'Kuwait'),
        ('Bahrain', 'Bahrain'),
        ('Oman', 'Oman'),
        ('Turkey', 'Turkey'),
        ('Syria', 'Syria'),
        ('Iraq', 'Iraq'),
        ('Yemen', 'Yemen'),
    ]

    CITY_CHOICES = [
        ('', 'Select City'),
    ]

    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
            'id': 'tour-country-select'
        })
    )

    city = forms.ChoiceField(
        choices=CITY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
            'id': 'tour-city-select',
            'disabled': True
        })
    )

    class Meta:
        model = Tour
        fields = ['host_name', 'contact_email', 'contact_phone', 'certifications', 'tour_name', 'tour_category', 'duration', 'country', 'city', 'languages', 'min_participants', 'max_participants', 'age_restrictions', 'tagline', 'full_description', 'itinerary', 'meeting_point', 'end_point', 'highlights', 'inclusions', 'exclusions', 'fitness_level', 'safety_gear', 'cancellation_policy', 'price_per_person', 'group_price', 'child_discount', 'currency']
        widgets = {
            'host_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'certifications': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'tour_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'tour_category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'languages': forms.SelectMultiple(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'size': '6'
            }),
            'min_participants': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'max_participants': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'age_restrictions': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'tagline': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'maxlength': 150
            }),
            'full_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'rows': 6
            }),
            'itinerary': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'rows': 8
            }),
            'meeting_point': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'end_point': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'highlights': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'rows': 4
            }),
            'inclusions': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'exclusions': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'rows': 6
            }),
            'fitness_level': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'safety_gear': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'rows': 3
            }),
            'cancellation_policy': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'price_per_person': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'step': '0.01'
            }),
            'group_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'step': '0.01'
            }),
            'child_discount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'currency': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
        }


class TourGuideForm(forms.ModelForm):
    """Form for creating/editing tour guide profiles"""

    # Country and City choices
    COUNTRY_CHOICES = [
        ('', 'Select Country'),
        ('Jordan', 'Jordan'),
        ('UAE', 'United Arab Emirates'),
        ('Egypt', 'Egypt'),
        ('Lebanon', 'Lebanon'),
        ('Qatar', 'Qatar'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Kuwait', 'Kuwait'),
        ('Bahrain', 'Bahrain'),
        ('Oman', 'Oman'),
        ('Turkey', 'Turkey'),
        ('Syria', 'Syria'),
        ('Iraq', 'Iraq'),
        ('Yemen', 'Yemen'),
    ]

    CITY_CHOICES = [
        ('', 'Select City'),
    ]

    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
            'id': 'guide-country-select'
        })
    )

    city = forms.ChoiceField(
        choices=CITY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
            'id': 'guide-city-select',
            'disabled': True
        })
    )

    class Meta:
        model = TourGuide
        exclude = ['host', 'created_at', 'updated_at']
        widgets = {
            'guide_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'placeholder': 'Full name'
            }),
            'tagline': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'placeholder': 'e.g., Expert historian with 10 years experience'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'rows': 5,
                'placeholder': 'Tell potential clients about your experience, expertise, and what makes you unique...'
            }),
            'license_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500'
            }),
            'certifications': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'rows': 3,
                'placeholder': 'List your certifications (comma-separated)'
            }),
            'years_experience': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'min': '0'
            }),
            'languages': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'placeholder': 'e.g., English, Arabic, French'
            }),
            'specializations': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'placeholder': 'e.g., Historical Sites, Cultural Tours, Adventure'
            }),
            'hourly_rate': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'step': '0.01'
            }),
            'half_day_rate': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'step': '0.01'
            }),
            'full_day_rate': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'step': '0.01'
            }),
            'max_group_size': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'min': '1'
            }),
            'service_area': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'rows': 3,
                'placeholder': 'List areas/cities where you provide services'
            }),
            'minimum_booking_hours': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'min': '1'
            }),
            'cancellation_policy': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'rows': 3
            }),
            'terms_and_conditions': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'rows': 3
            }),
            'available_days': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'placeholder': 'e.g., Monday, Tuesday, Wednesday'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'placeholder': '+1 234 567 8900'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'placeholder': 'your@email.com'
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'placeholder': 'https://yourwebsite.com'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'placeholder': 'Emergency contact name and phone'
            }),
            'tour_types_offered': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'rows': 3,
                'placeholder': 'e.g., Walking tours, Private tours, Group tours, Bus tours'
            }),
            'equipment_provided': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'rows': 3,
                'placeholder': 'e.g., Audio guides, Maps, Water bottles, Snacks'
            }),
            'accessibility': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'rows': 2,
                'placeholder': 'e.g., Wheelchair accessible, Family-friendly, Senior-friendly'
            }),
            'covid_safety': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500',
                'rows': 2,
                'placeholder': 'e.g., Masks provided, Small groups, Sanitized equipment'
            }),
        }


class RentalCarForm(forms.ModelForm):
    """Form for creating/editing rental car listings"""

    # Country and City choices
    COUNTRY_CHOICES = [
        ('', 'Select Country'),
        ('Jordan', 'Jordan'),
        ('UAE', 'United Arab Emirates'),
        ('Egypt', 'Egypt'),
        ('Lebanon', 'Lebanon'),
        ('Qatar', 'Qatar'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Kuwait', 'Kuwait'),
        ('Bahrain', 'Bahrain'),
        ('Oman', 'Oman'),
        ('Turkey', 'Turkey'),
        ('Syria', 'Syria'),
        ('Iraq', 'Iraq'),
        ('Yemen', 'Yemen'),
    ]

    CITY_CHOICES = [
        ('', 'Select City'),
    ]

    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
            'id': 'car-country-select'
        })
    )

    city = forms.ChoiceField(
        choices=CITY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
            'id': 'car-city-select',
            'disabled': True
        })
    )

    class Meta:
        model = RentalCar
        exclude = ['host', 'created_at', 'updated_at']
        widgets = {
            'vehicle_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'placeholder': 'e.g., Toyota Camry 2023'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'placeholder': 'Toyota'
            }),
            'model': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'placeholder': 'Camry'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'min': '1990',
                'max': '2030'
            }),
            'vehicle_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500'
            }),
            'tagline': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'placeholder': 'Brief description of the vehicle'
            }),
            'full_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'rows': 5,
                'placeholder': 'Describe the vehicle condition, features, and what makes it special...'
            }),
            'transmission': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500'
            }),
            'fuel_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500'
            }),
            'seating_capacity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'min': '2',
                'max': '15'
            }),
            'doors': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'min': '2',
                'max': '6'
            }),
            'luggage_capacity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'min': '0'
            }),
            'features': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'placeholder': 'e.g., GPS, AC, Bluetooth, USB, Backup Camera'
            }),
            'daily_rate': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'step': '0.01'
            }),
            'weekly_rate': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'step': '0.01'
            }),
            'monthly_rate': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'step': '0.01'
            }),
            'security_deposit': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'step': '0.01'
            }),
            'insurance_cost_per_day': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'step': '0.01'
            }),
            'mileage_limit_per_day': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'min': '0'
            }),
            'extra_mileage_cost': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'step': '0.01'
            }),
            'pickup_location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'placeholder': 'Address where customers can pick up the vehicle'
            }),
            'delivery_fee': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'step': '0.01'
            }),
            'minimum_age': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'min': '18',
                'max': '80'
            }),
            'minimum_license_years': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'min': '0'
            }),
            'minimum_rental_days': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'min': '1'
            }),
            'cancellation_policy': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'rows': 3
            }),
            'fuel_policy': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500'
            }),
            'odometer_reading': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'min': '0'
            }),
            'condition': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'placeholder': 'e.g., Excellent, Very Good, Good'
            }),
            'terms_and_conditions': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'rows': 3
            }),
            'color': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'placeholder': 'e.g., Black, White, Silver'
            }),
            'license_plate': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'placeholder': 'ABC-1234'
            }),
            'vin_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'placeholder': '17-character VIN'
            }),
            'registration_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500'
            }),
            'owner_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'placeholder': 'Vehicle owner name'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'placeholder': '+1 234 567 8900'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'placeholder': 'contact@email.com'
            }),
            'late_return_fee': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'step': '0.01'
            }),
            'cleaning_fee': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500',
                'step': '0.01'
            }),
        }