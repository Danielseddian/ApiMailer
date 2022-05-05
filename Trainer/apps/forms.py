from django import forms


class ResolveForm(forms.Form):
    renewal_date = forms.CharField(max_length=5000, required=True)
