from django.views import View
from django.http import HttpResponseRedirect
from payment import forms
from django.urls import reverse
from urlparse import parse_qs
from catalogue import models as catalogue_models

class SettlePlugnPayPaymentView(View):
    """
    settles a plugnpay payment based on the response received by the client
    """


    def post(self, request, *args, **kwargs):
        form = forms.PlugnPayPaymentForm(request.POST)
        course_id = self.kwargs.get("course_id")


        if form.is_valid():
           # pnp_response = form.instance
           # dict_pnp_response = parse_qs(pnp_response.response)
           #todo check if payment was successfully authorized by plugnpay
           catalogue_models.Enrollment.objects.get_or_create(product_id=course_id, user=request.user) 
           #todo settle payment here
           return HttpResponseRedirect(reverse('checkout:thank-you'))

        return HttpResponseRedirect(reverse('checkout:payment-details', kwargs={'course_id': course_id}))