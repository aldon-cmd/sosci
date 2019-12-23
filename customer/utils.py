from __future__ import absolute_import  # for import below
import logging
import django 
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from post_office import mail
import six

from unidecode import unidecode



def slugify(value):
    """
    Slugify a string (even if it contains non-ASCII chars)
    """

    from django.template import defaultfilters
    slugifier = defaultfilters.slugify

    # Use unidecode to convert non-ASCII strings to ASCII equivalents where
    # possible.
    value = slugifier(unidecode(six.text_type(value)))

    return value



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

        email = self.send_email_messages(user.email, messages)


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


def get_password_reset_url(user, token_generator=default_token_generator):
    """
    Generate a password-reset URL for a given user
    """
    kwargs = {'token': token_generator.make_token(user)}
    if django.VERSION < (1, 6):
        from django.utils.http import int_to_base36
        kwargs['uidb36'] = int_to_base36(user.id)
    else:
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        kwargs['uidb64'] = urlsafe_base64_encode(force_bytes(user.id))
    return reverse('auth:password-reset-confirm', kwargs=kwargs)

def normalise_email(email):
    """
    The local part of an email address is case-sensitive, the domain part
    isn't.  This function lowercases the host and should be used in all email
    handling.
    """
    clean_email = email.strip()
    if '@' in clean_email:
        local, host = clean_email.split('@')
        return local + '@' + host.lower()
    return clean_email