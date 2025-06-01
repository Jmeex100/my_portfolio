from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'id': 'name'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded', 'id': 'email'}),
            'message': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 4, 'id': 'message'}),
        }