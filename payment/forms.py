from django import forms


class PlugnPayPaymentForm(forms.ModelForm):
    response = forms.CharField(widget=forms.Textarea)