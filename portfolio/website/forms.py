# forms.py
from django import forms
from .models import ContactMessage
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone

class ContactForm(forms.ModelForm):
    # Optional: Add honeypot field for bot protection
    honeypot = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'hidden', 'tabindex': '-1', 'autocomplete': 'off'}),
        label='Leave this field empty'
    )
    
    # Add timestamp field for client-side time validation
    client_time = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300',
                'placeholder': 'Your name',
                'autocomplete': 'name',
                'id': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300',
                'placeholder': 'your@email.com',
                'autocomplete': 'email',
                'id': 'email'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300',
                'rows': 4,
                'placeholder': 'Your message here...',
                'id': 'message'
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'message': 'Your Message',
        }
        help_texts = {
            'name': 'Please enter your full name',
            'email': 'We\'ll never share your email with anyone else',
            'message': 'Please provide detailed information about your inquiry',
        }
        error_messages = {
            'name': {
                'required': 'Please enter your name',
                'max_length': 'Name is too long (maximum 100 characters)',
            },
            'email': {
                'required': 'Please enter your email address',
                'invalid': 'Please enter a valid email address',
            },
            'message': {
                'required': 'Please enter your message',
            },
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Add required attribute for accessibility
        for field_name in self.fields:
            if field_name not in ['honeypot', 'client_time']:
                self.fields[field_name].widget.attrs['aria-required'] = 'true'

    def clean_honeypot(self):
        """Honeypot validation for bot protection"""
        honeypot = self.cleaned_data.get('honeypot')
        if honeypot:
            raise ValidationError('This form submission appears to be automated.')
        return honeypot

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if not email:
            return email
            
        # Check for recent submissions (5 minutes cooldown)
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        recent_messages = ContactMessage.objects.filter(
            email=email,
            created_at__gte=five_minutes_ago
        )
        
        if recent_messages.exists():
            raise ValidationError(
                'Please wait at least 5 minutes before sending another message.'
            )
        
        # Also check by IP if request is available
        if self.request:
            ip_address = self.get_client_ip()
            if ip_address:
                recent_by_ip = ContactMessage.objects.filter(
                    ip_address=ip_address,
                    created_at__gte=five_minutes_ago
                )
                
                if recent_by_ip.exists():
                    raise ValidationError(
                        'Please wait at least 5 minutes before sending another message.'
                    )
        
        return email

    def clean_client_time(self):
        """Optional: Validate client timestamp to prevent rapid submissions"""
        client_time = self.cleaned_data.get('client_time')
        
        if client_time and self.request:
            try:
                # Convert timestamp to datetime
                from datetime import datetime
                import time
                
                # This is a basic check - you can implement more sophisticated timing
                # For example, ensure form wasn't submitted too quickly (< 3 seconds)
                if 'form_start_time' in self.request.session:
                    form_start_time = self.request.session['form_start_time']
                    submission_time = time.time()
                    
                    # If form was submitted in less than 3 seconds, likely automated
                    if submission_time - form_start_time < 3:
                        raise ValidationError('Form submitted too quickly. Please try again.')
            except:
                pass  # Don't block if timestamp validation fails
        
        return client_time

    def get_client_ip(self):
        """Extract client IP address from request"""
        if not self.request:
            return None
            
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def save(self, commit=True, request=None):
        """Override save to add IP address and user agent"""
        instance = super().save(commit=False)
        
        if request:
            # Get client IP
            instance.ip_address = self.get_client_ip()
            
            # Get user agent
            instance.user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Remove honeypot field from data
            if 'honeypot' in self.cleaned_data:
                del self.cleaned_data['honeypot']
            if 'client_time' in self.cleaned_data:
                del self.cleaned_data['client_time']
        
        if commit:
            instance.save()
            
            # Store submission time in session for cooldown tracking
            if request:
                request.session['last_submission_time'] = timezone.now().isoformat()
                request.session['last_submission_email'] = self.cleaned_data.get('email', '')
        
        return instance

    def get_cooldown_remaining(self, email=None):
        """Get remaining cooldown time for this form submission"""
        if not email:
            email = self.cleaned_data.get('email') if self.is_bound else None
            
        if email:
            return ContactMessage.get_cooldown_remaining(email)
        
        # Also check by IP if request is available
        if self.request:
            ip_address = self.get_client_ip()
            if ip_address:
                return ContactMessage.get_cooldown_remaining_by_ip(ip_address)
        
        return 0

    def is_in_cooldown(self, email=None):
        """Check if the form is currently in cooldown period"""
        return self.get_cooldown_remaining(email) > 0


# Optional: Form mixin for rate limiting
class RateLimitedFormMixin:
    """Mixin to add rate limiting to any form"""
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Apply rate limiting logic here if needed
        # This is a template for other forms you might create
        
        return cleaned_data