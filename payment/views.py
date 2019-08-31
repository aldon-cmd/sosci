from django.views import View
from django.http import HttpResponseRedirect
from payment import forms
from django.urls import reverse
from urlparse import parse_qs

class SettlePlugnPayPaymentView(View):
    """
    settles a plugnpay payment based on the response received by the client
    """
    form_class = forms.PlugnPayPaymentForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        course_id = self.kwargs.get("course_id")


        if form.is_valid():
           pnp_response = form.instance
           dict_pnp_response = parse_qs(pnp_response.response)
           #todo settle payment here
           return HttpResponseRedirect('/success/')

        return HttpResponseRedirect(reverse('checkout:payment-details', kwargs={'course_id': course_id}))