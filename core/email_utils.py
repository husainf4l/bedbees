"""
Email Utility Functions for BedBees
Handles email notifications for listing publishing, approvals, and rejections.
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_listing_published_email(listing, listing_type='accommodation'):
    """
    Send confirmation email when a listing is published.
    
    Args:
        listing: The listing object (Accommodation, Tour, RentalCar, etc.)
        listing_type: Type of listing ('accommodation', 'tour', 'rental_car', 'taxi')
    """
    # Get listing details
    if listing_type == 'accommodation':
        listing_name = listing.property_name
        location = f"{listing.city}, {listing.country}"
    elif listing_type == 'tour':
        listing_name = listing.tour_name
        location = f"{listing.city}, {listing.country}"
    elif listing_type == 'rental_car':
        listing_name = f"{listing.brand} {listing.model} ({listing.year})"
        location = f"{listing.city}, {listing.country}"
    else:
        listing_name = "Your Listing"
        location = "N/A"
    
    # Get host email
    host_email = listing.host.email
    host_name = listing.host.get_full_name() or listing.host.username
    
    # Email subject
    subject = f"🎉 Your listing is now live on BedBees!"
    
    # Email body
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2563eb;">Congratulations, {host_name}!</h2>
            
            <p>Your listing "<strong>{listing_name}</strong>" in <strong>{location}</strong> is now published and visible to travelers worldwide! 🌍</p>
            
            <div style="background-color: #f0f9ff; border-left: 4px solid #2563eb; padding: 15px; margin: 20px 0;">
                <h3 style="margin-top: 0;">What happens next?</h3>
                <ul>
                    <li>Your listing is now searchable on BedBees</li>
                    <li>Travelers can view and book your {listing_type}</li>
                    <li>You'll receive notifications for inquiries and bookings</li>
                    <li>Track your performance in the Host Dashboard</li>
                </ul>
            </div>
            
            <div style="margin: 30px 0;">
                <a href="{settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000'}/hostdashboard/" 
                   style="background-color: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    View Your Dashboard
                </a>
            </div>
            
            <p style="color: #666; font-size: 14px; margin-top: 30px;">
                Need help? Contact us at support@bedbees.com or visit our Help Center.
            </p>
            
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
            
            <p style="color: #999; font-size: 12px;">
                You're receiving this email because you published a listing on BedBees.<br>
                BedBees - Connecting Travelers Worldwide
            </p>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@bedbees.com',
            recipient_list=[host_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_listing_approved_email(listing, listing_type='accommodation'):
    """
    Send email when a listing is approved by admin.
    
    Args:
        listing: The listing object
        listing_type: Type of listing
    """
    # Get listing details
    if listing_type == 'accommodation':
        listing_name = listing.property_name
        location = f"{listing.city}, {listing.country}"
    elif listing_type == 'tour':
        listing_name = listing.tour_name
        location = f"{listing.city}, {listing.country}"
    elif listing_type == 'rental_car':
        listing_name = f"{listing.brand} {listing.model}"
        location = f"{listing.city}, {listing.country}"
    else:
        listing_name = "Your Listing"
        location = "N/A"
    
    host_email = listing.host.email
    host_name = listing.host.get_full_name() or listing.host.username
    
    subject = f"✅ Your listing has been approved!"
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #10b981;">Great News, {host_name}!</h2>
            
            <p>Your {listing_type} "<strong>{listing_name}</strong>" in <strong>{location}</strong> has been approved and is now live on our platform! 🎊</p>
            
            <div style="background-color: #f0fdf4; border-left: 4px solid #10b981; padding: 15px; margin: 20px 0;">
                <p style="margin: 0;"><strong>Status:</strong> Approved & Published</p>
                <p style="margin: 10px 0 0 0;"><strong>Listed on:</strong> {listing.published_at.strftime('%B %d, %Y') if listing.published_at else 'Now'}</p>
            </div>
            
            <p>Your listing meets our quality standards and is now available for bookings.</p>
            
            <div style="margin: 30px 0;">
                <a href="{settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000'}/hostdashboard/" 
                   style="background-color: #10b981; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    View Your Dashboard
                </a>
            </div>
            
            <p style="color: #666; font-size: 14px;">
                Thank you for being a valued host on BedBees! 🙏
            </p>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@bedbees.com',
            recipient_list=[host_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_listing_rejected_email(listing, listing_type='accommodation', reason=''):
    """
    Send email when a listing is rejected by admin.
    
    Args:
        listing: The listing object
        listing_type: Type of listing
        reason: Reason for rejection
    """
    # Get listing details
    if listing_type == 'accommodation':
        listing_name = listing.property_name
    elif listing_type == 'tour':
        listing_name = listing.tour_name
    elif listing_type == 'rental_car':
        listing_name = f"{listing.brand} {listing.model}"
    else:
        listing_name = "Your Listing"
    
    host_email = listing.host.email
    host_name = listing.host.get_full_name() or listing.host.username
    
    subject = f"⚠️ Action required: Your listing needs attention"
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #dc2626;">Action Required, {host_name}</h2>
            
            <p>Your {listing_type} "<strong>{listing_name}</strong>" requires some updates before it can be published.</p>
            
            <div style="background-color: #fef2f2; border-left: 4px solid #dc2626; padding: 15px; margin: 20px 0;">
                <h3 style="margin-top: 0; color: #dc2626;">Reason for Review:</h3>
                <p style="margin: 0;">{reason if reason else 'Please review your listing details and make necessary corrections.'}</p>
            </div>
            
            <h3>Next Steps:</h3>
            <ol>
                <li>Review your listing details carefully</li>
                <li>Make the necessary corrections</li>
                <li>Submit your listing again for review</li>
            </ol>
            
            <div style="margin: 30px 0;">
                <a href="{settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000'}/hostdashboard/" 
                   style="background-color: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Edit Your Listing
                </a>
            </div>
            
            <p style="color: #666; font-size: 14px;">
                If you have questions, please don't hesitate to contact our support team at support@bedbees.com
            </p>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@bedbees.com',
            recipient_list=[host_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_listing_edit_notification(listing, listing_type='accommodation'):
    """
    Send notification to host that their edit is pending approval.
    
    Args:
        listing: The listing object
        listing_type: Type of listing
    """
    host_email = listing.host.email
    host_name = listing.host.get_full_name() or listing.host.username
    
    if listing_type == 'accommodation':
        listing_name = listing.property_name
    elif listing_type == 'tour':
        listing_name = listing.tour_name
    elif listing_type == 'rental_car':
        listing_name = f"{listing.brand} {listing.model}"
    else:
        listing_name = "Your Listing"
    
    subject = f"📝 Your listing update is under review"
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2563eb;">Update Received, {host_name}!</h2>
            
            <p>Thank you for updating your {listing_type} "<strong>{listing_name}</strong>".</p>
            
            <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 20px 0;">
                <p style="margin: 0;">Your changes are currently under review by our team. We'll notify you once they're approved and live.</p>
            </div>
            
            <p>Your listing will remain visible with the previous information until the changes are approved.</p>
            
            <p style="color: #666; font-size: 14px;">
                We typically review updates within 24-48 hours.
            </p>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@bedbees.com',
            recipient_list=[host_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
