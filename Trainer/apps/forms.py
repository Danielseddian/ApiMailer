from django import forms
from django.db import models


class ResolveForm(forms.Form):
    resolve = forms.CharField(max_length=5000, required=True, widget=forms.Textarea)
