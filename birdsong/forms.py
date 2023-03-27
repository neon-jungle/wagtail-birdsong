from django import forms
from birdsong.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('email',)
