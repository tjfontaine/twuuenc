from django import forms

class EncodeForm(forms.Form):
  input = forms.CharField(required=False, widget=forms.Textarea, max_length=512)
  output = forms.CharField(required=False, widget=forms.Textarea, max_length=512)
  compress = forms.BooleanField(required=False)
  markers = forms.BooleanField(required=False)
