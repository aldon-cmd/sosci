import pandas
import logging
from django.urls import reverse
from customer.utils import create_email_activation_key
from custom_user import models as custom_user_models
from django.contrib.sites.shortcuts import get_current_site
import hashlib, datetime, random
from customer import models as customer_models
from custom_user import models as custom_user_models
from customer.utils import create_email_activation_key
from catalogue.helpers import Course
from django.conf import settings
from post_office import mail

class UserRegistration(object):

    def register_user(self, form,request):
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


        self.send_confirmation_email(user,request)
        
        return user

    def get_or_create_student(self,form,request):

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
            self.send_registration_email(user,request)
        else:
            user = custom_user_models.User.objects.filter(email=email).first()
            self.send_registration_email(user,request)

        return user

    def register_inactive_user(self,form,request):

        course_id = form.cleaned_data.pop('course')
        student = self.get_or_create_student(form,request)

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



    def send_registration_email(self, user, request):
        code = 'REGISTRATION'
        ctx = {'user': user,
               'site': get_current_site(request)}
        messages = customer_models.CommunicationEventType.objects.get_and_render(
            code, ctx)
        if messages and messages['body']:
            Dispatcher().dispatch_user_messages(user, messages)


class Dispatcher(object):
    def __init__(self, logger=None):
        if not logger:
            logger = logging.getLogger(__name__)
        self.logger = logger

    # Public API methods

    def dispatch_direct_messages(self, recipient, messages):
        """
        Dispatch one-off messages to explicitly specified recipient(s).
        """
        if messages['subject'] and messages['body']:
            self.send_email_messages(recipient, messages)

    def dispatch_order_messages(self, order, messages, event_type=None,
                                **kwargs):
        """
        Dispatch order-related messages to the customer
        """
        if order.is_anonymous:
            if 'email_address' in kwargs:
                self.send_email_messages(kwargs['email_address'], messages)
            elif order.guest_email:
                self.send_email_messages(order.guest_email, messages)
            else:
                return
        else:
            self.dispatch_user_messages(order.user, messages)

    def dispatch_user_messages(self, user, messages):
        """
        Send messages to a site user
        """
        if messages['subject'] and (messages['body'] or messages['html']):
            self.send_user_email_messages(user, messages)
        if messages['sms']:
            self.send_text_message(user, messages['sms'])

    # Internal

    def send_user_email_messages(self, user, messages):
        """
        Sends message to the registered user / customer and collects data in
        database
        """
        if not user.email:
            self.logger.warning("Unable to send email messages as user #%d has"
                                " no email address", user.id)
            return

        self.send_email_messages(user.email, messages)


    def send_email_messages(self, recipient, messages):
        """
        Plain email sending to the specified recipient
        """
        if hasattr(settings, 'OSCAR_FROM_EMAIL'):
            from_email = settings.OSCAR_FROM_EMAIL
        else:
            from_email = None

        # Determine whether we are sending a HTML version too
        if messages['html']:
            self.logger.info("Sending email to %s" % recipient)
            email = mail.send([recipient],'sales@pantrypan.com', subject=messages['subject'], message=messages['body'], html_message=messages['html'],)
            # email = EmailMultiAlternatives(messages['subject'],
            #                                messages['body'],
            #                                from_email=from_email,
            #                                to=[recipient])
            # email.attach_alternative(messages['html'], "text/html")
        else:
            self.logger.info("Sending email to %s" % recipient)
            email = mail.send([recipient],'sales@pantrypan.com', subject=messages['subject'], message=messages['body'],)
            # email = EmailMessage(messages['subject'],
            #                      messages['body'],
            #                      from_email=from_email,
            #                      to=[recipient])
        # self.logger.info("Sending email to %s" % recipient)
        # email.send()

        return email

    def send_text_message(self, user, event_type):
        raise NotImplementedError

class CSVUploader(object):


    def __init__(self, csv_file):
        self.csv_file = csv_file

        self.dataframe = pandas.read_csv(self.csv_file,usecols=["Email Address",]).fillna('')

        self.dataframe_required_fields = self.dataframe[["Email",]]

        required_fields = self.dataframe_required_fields.columns[self.dataframe_required_fields.isin(['']).any()].tolist()

        if len(required_fields) > 0:
          raise ValueError('these fields are required: ' + ' '.join(required_fields))

        #rename columns. replaces spaces with underscores
        self.dataframe.columns = [col.replace(' ', '_') for col in self.dataframe.columns]

        self.column_names = self.dataframe.columns.values.tolist()

#     def upload(self):
#         # row.Vacation_Days_Oustanding


#         with transaction.atomic():

#               self.create_employees()

#               for row in self.dataframe.itertuples():
                  
#                 annual_salary_sum = 0.00
#                 previous_payperiod = self.select_previous_payperiod(row.Pay_Frequency_Type.title())
#                 current_payperiod = self.get_current_payperiod(row.Pay_Frequency_Type.title())
#                 #loop over salary adjustments by column(going across in a horizontal direction)
#                 for i in range(len(self.column_names)-31):
#                     current_column = self.column_names[i+31]
#                     amount = float(self.dataframe.at[row.Index,current_column])
#                     #skip annual salary adjustments that are not greater than zero
#                     if amount > 0.00:
#                       annual_salary_sum += amount
#                       annual_salary = self.create_annual_salary_adjustment(current_column,amount,self.employees[row.Index])
#                       self.create_annual_salaries_list(current_column,row,annual_salary,current_payperiod)


#                 self.create_employee_employment_details_list(row,annual_salary_sum)

#                 self.create_paidtimeoff(row)

#                 #a payroll record should not be created at the beginning of the year
#                 if previous_payperiod is not None:
#                    self.create_payroll(row,previous_payperiod)
              
#               models.EmployeeEmploymentDetail.objects.bulk_create(self.employeeemploymentdetails)

#               models.AnnualSalary.objects.bulk_create(self.annual_salaries)

#               models.AnnualSalary.objects.bulk_create(self.annual_allowance_salaries)

#               self.create_salaries_list(self.annual_salaries,self.salaries,current_payperiod)

#               self.create_salaries_list(self.annual_allowance_salaries,self.allowance_salaries,current_payperiod)

              
#               models.Salary.objects.bulk_create(self.salaries)

#               models.Salary.objects.bulk_create(self.allowance_salaries)

#               self.create_taxexemptions()

#               #n/b Payroll records should be optional 
#               models.Payroll.objects.bulk_create(self.payrolls)