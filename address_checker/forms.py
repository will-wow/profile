from django import forms

class AddressForm(forms.Form):
    address1 = forms.CharField()
    address2 = forms.CharField(required=False)
    has_attn = forms.BooleanField(required=False)
