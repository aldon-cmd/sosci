from django import forms


class PlugnPayPaymentForm(forms.Form):
    response = forms.CharField(widget=forms.Textarea,required=False)