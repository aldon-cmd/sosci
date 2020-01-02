from django.contrib.sites.shortcuts import get_current_site
import hashlib, datetime, random
from customer import models as customer_models
from custom_user import models as custom_user_models
from customer.utils import Dispatcher, create_email_activation_key
from catalogue.utils import Course

class RegisterUserMixin(object):

    def register_user(self, form):
        """
        Create a user instance and send a new registration email (if configured
        to).
        """
        email = form.cleaned_data['email']           
        activation_key = create_email_activation_key(email)           
        key_expires = datetime.datetime.today() + datetime.timedelta(2)

        user = form.save(commit=False)
        user.userrole = custom_user_models.UserRole.objects.filter(name="Student").first()
        user.activation_key = activation_key
        user.key_expires = key_expires
        user.save()


        self.send_confirmation_email(user,self.request)
        
        return user

    def get_or_create_student(self,form):

        email = form.cleaned_data.pop('email')
        password = None
        user = None

        if not custom_user_models.User.objects.filter(email=email).exists():
            password = custom_user_models.User.objects.make_random_password(length=6)
            user = custom_user_models.User.objects.create_user(
                            email,
                            password,
                            **form.cleaned_data
                        )
            self.send_registration_email(user,self.request)
        else:
            user = custom_user_models.User.objects.filter(email=email).first()
            self.send_registration_email(user,self.request)

        return user

    def register_inactive_user(self,form):

        course_id = form.cleaned_data.pop('course')
        student = self.get_or_create_student(form)

        Course().enroll(student,course_id)

    def send_confirmation_email(self, user, request):
        code = "CONFIRMATION"
        ctx = {'user': user,
               'activation_key' : user.activation_key,
               'site': get_current_site(request)}
        messages = customer_models.CommunicationEventType.objects.get_and_render(
            code, ctx)
        if messages and messages['body']:
            Dispatcher().dispatch_user_messages(user, messages)



    def send_registration_email(self, user,request):
        code = 'REGISTRATION'
        ctx = {'user': user,
               'site': get_current_site(self.request)}
        messages = customer_models.CommunicationEventType.objects.get_and_render(
            code, ctx)
        if messages and messages['body']:
            Dispatcher().dispatch_user_messages(user, messages)
