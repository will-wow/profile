from django import forms

class ContactEmail(forms.Form):
    emailfrom = forms.EmailField()
    email = forms.CharField()