from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_honeypot(self):
        if self.cleaned_data.get('honeypot'):
            raise ValidationError("Invalid submission.")
        return self.cleaned_data.get('honeypot')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email

        cooldown_time = timezone.now() - timedelta(minutes=1)

        if ContactMessage.objects.filter(
            email=email,
            created_at__gte=cooldown_time
        ).exists():
            raise ValidationError(
                "Please wait  minutes before sending another message."
            )

        return email

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.request:
            instance.ip_address = self.get_client_ip()
            instance.user_agent = self.request.META.get('HTTP_USER_AGENT', '')

        if commit:
            instance.save()

        return instance

    def get_client_ip(self):
        if not self.request:
            return None

        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]

        return self.request.META.get('REMOTE_ADDR')
