from django import forms

class EncodeForm(forms.Form):
  input = forms.CharField(required=False, widget=forms.Textarea)
  output = forms.CharField(required=False, widget=forms.Textarea)
  compress = forms.BooleanField(required=False)
