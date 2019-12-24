from django.contrib.sites.shortcuts import get_current_site
import hashlib, datetime, random
from customer import models as customer_models
from custom_user import models as custom_user_models
from customer.utils import Dispatcher 



class RegisterUserMixin(object):
    communication_type_code = 'REGISTRATION'

    def register_user(self, form):
        """
        Create a user instance and send a new registration email (if configured
        to).
        """
        email = form.cleaned_data['email']
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]            
        activation_key = hashlib.sha1((salt+email).encode('utf-8')).hexdigest()            
        key_expires = datetime.datetime.today() + datetime.timedelta(2)

        user = form.save(commit=False)
        user.userrole = custom_user_models.UserRole.objects.filter(name="Student").first()
        user.activation_key = activation_key
        user.key_expires = key_expires
        user.save()

        # Raise signal robustly (we don't want exceptions to crash the request
        # handling).
        # user_registered.send_robust(
        #     sender=self, request=self.request, user=user)

        self.send_confirmation_email(user,self.request)
        
        # if getattr(settings, 'OSCAR_SEND_REGISTRATION_EMAIL', True):
        #     self.send_registration_email(user)

        # We have to authenticate before login
        # try:
        #     user = authenticate(
        #         username=user.email,
        #         password=form.cleaned_data['password1'])
        # except User.MultipleObjectsReturned:
        #     # Handle race condition where the registration request is made
        #     # multiple times in quick succession.  This leads to both requests
        #     # passing the uniqueness check and creating users (as the first one
        #     # hasn't committed when the second one runs the check).  We retain
        #     # the first one and delete the dupes.
        #     users = User.objects.filter(email=user.email)
        #     user = users[0]
        #     for u in users[1:]:
        #         u.delete()

        # auth_login(self.request, user)

        return user

    def send_confirmation_email(self, user, request):
        code = "CONFIRMATION"
        ctx = {'user': user,
               'activation_key' : user.activation_key,
               'site': get_current_site(request)}
        messages = customer_models.CommunicationEventType.objects.get_and_render(
            code, ctx)
        if messages and messages['body']:
            Dispatcher().dispatch_user_messages(user, messages)



    def send_registration_email(self, user):
        code = self.communication_type_code
        ctx = {'user': user,
               'site': get_current_site(self.request)}
        messages = customer_models.CommunicationEventType.objects.get_and_render(
            code, ctx)
        if messages and messages['body']:
            Dispatcher().dispatch_user_messages(user, messages)
