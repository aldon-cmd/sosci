from django.conf import settings
from django.db import models
from django.template import Template, TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from customer.fields import AutoSlugField
from customer.managers import CommunicationTypeManager


class CommunicationEventType(models.Model):
    """
    A 'type' of communication.  Like a order confirmation email.
    """

    #: Code used for looking up this event programmatically.
    # e.g. PASSWORD_RESET. AutoSlugField uppercases the code for us because
    # it's a useful convention that's been enforced in previous Oscar versions
    code = AutoSlugField(
        _('Code'), max_length=128, unique=True, populate_from='name',
        separator="_", uppercase=True, editable=True,
        help_text=_("Code used for looking up this event programmatically"))

    #: Name is the friendly description of an event for use in the admin
    name = models.CharField(
        _('Name'), max_length=255,
        help_text=_("This is just used for organisational purposes"))

    # We allow communication types to be categorised
    ORDER_RELATED = _('Order related')
    USER_RELATED = _('User related')
    category = models.CharField(_('Category'), max_length=255,
                                default=USER_RELATED)

    # Template content for emails
    # NOTE: There's an intentional distinction between None and ''. None
    # instructs Oscar to look for a file-based template, '' is just an empty
    # template.
    email_subject_template = models.CharField(
        _('Email Subject Template'), max_length=255, blank=True, null=True)
    email_body_template = models.TextField(
        _('Email Body Template'), blank=True, null=True)
    email_body_html_template = models.TextField(
        _('Email Body HTML Template'), blank=True, null=True,
        help_text=_("HTML template"))

    # Template content for SMS messages
    sms_template = models.CharField(_('SMS Template'), max_length=170,
                                    blank=True, null=True,
                                    help_text=_("SMS template"))

    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True)

    objects = CommunicationTypeManager()

    # File templates
    email_subject_template_file = 'customer/emails/commtype_%s_subject.txt'
    email_body_template_file = 'customer/emails/commtype_%s_body.txt'
    email_body_html_template_file = 'customer/emails/commtype_%s_body.html'
    sms_template_file = 'customer/sms/commtype_%s_body.txt'

    class Meta:
        verbose_name = _("Communication event type")
        verbose_name_plural = _("Communication event types")

    def get_messages(self, ctx=None):
        """
        Return a dict of templates with the context merged in
        We look first at the field templates but fail over to
        a set of file templates that follow a conventional path.
        """
        code = self.code.lower()

        # Build a dict of message name to Template instances
        templates = {'subject': 'email_subject_template',
                     'body': 'email_body_template',
                     'html': 'email_body_html_template',
                     'sms': 'sms_template'}
        for name, attr_name in templates.items():
            field = getattr(self, attr_name, None)
            if field is not None:
                # Template content is in a model field
                templates[name] = Template(field)
            else:
                # Model field is empty - look for a file template
                template_name = getattr(self, "%s_file" % attr_name) % code
                try:
                    templates[name] = get_template(template_name)
                except TemplateDoesNotExist:
                    templates[name] = None

        # Pass base URL for serving images within HTML emails
        if ctx is None:
            ctx = {}
        ctx['static_base_url'] = getattr(
            settings, 'OSCAR_STATIC_BASE_URL', None)

        messages = {}
        for name, template in templates.items():
            messages[name] = template.render(ctx) if template else ''

        # Ensure the email subject doesn't contain any newlines
        messages['subject'] = messages['subject'].replace("\n", "")
        messages['subject'] = messages['subject'].replace("\r", "")

        return messages

    def __str__(self):
        return self.name

    def is_order_related(self):
        return self.category == self.ORDER_RELATED

    def is_user_related(self):
        return self.category == self.USER_RELATED

from oscar.apps.customer.models import *  # noqa isort:skip
