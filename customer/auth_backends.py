from django.contrib.auth.backends import ModelBackend
from django.core.mail import mail_admins
from django.core.exceptions import ImproperlyConfigured

from django.contrib.auth import get_user_model

User = get_user_model()

if hasattr(User, 'REQUIRED_FIELDS'):
    if not (User.USERNAME_FIELD == 'email' or 'email' in User.REQUIRED_FIELDS):
        raise ImproperlyConfigured(
            "Emailbackend: Your User model must have an email"
            " field with blank=False")


class Emailbackend(ModelBackend):
    """
    Custom auth backend that uses an email address and password

    For this to work, the User model must have an 'email' field
    """

    def authenticate(self, email=None, password=None, *args, **kwargs):
        if email is None:
            if not 'username' in kwargs or kwargs['username'] is None:
                return None
            clean_email = self.normalise_email(kwargs['username'])
        else:
            clean_email = self.normalise_email(email)

        # Check if we're dealing with an email address
        if '@' not in clean_email:
            return None

        # Since Django doesn't enforce emails to be unique, we look for all
        # matching users and try to authenticate them all.  If we get more than
        # one success, then we mail admins as this is a problem.
        authenticated_users = []
        matching_users = User.objects.filter(email=clean_email)
        for user in matching_users:
            if user.check_password(password):
                authenticated_users.append(user)
        if len(authenticated_users) == 1:
            # Happy path
            return authenticated_users[0]
        elif len(authenticated_users) > 1:
            # This is the problem scenario where we have multiple users with
            # the same email address AND password.  We can't safely authentiate
            # either.  This situation requires intervention by an admin and so
            # we mail them to let them know!
            mail_admins(
                "There are multiple users with email address: %s"
                % clean_email,
                ("There are %s users with email %s and the same password "
                 "which means none of them are able to authenticate")
                % (len(authenticated_users), clean_email))
        return None

    def normalise_email(self,email):
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