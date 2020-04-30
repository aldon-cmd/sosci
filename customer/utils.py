from __future__ import absolute_import  # for import below
import logging
import django
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from post_office import mail
import six
import hashlib, random
from unidecode import unidecode

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
    
def create_email_activation_key(email):
    salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]            
    activation_key = hashlib.sha1((salt+email).encode('utf-8')).hexdigest()
    return activation_key

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