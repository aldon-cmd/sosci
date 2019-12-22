"""
Django settings for sosci project.

Generated by 'django-admin startproject' using Django 1.11.20.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from oscar import get_core_apps
from django.core.urlresolvers import reverse_lazy
import dj_database_url
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

location = lambda x: os.path.join(BASE_DIR, x)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!

#any string is True and empty strings are False
DEBUG = (os.environ.get('DEBUG', False) == 'True')

ALLOWED_HOSTS = ["*"]

DEFAULT_FROM_EMAIL = 'sosci2020@gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587

POST_OFFICE = {
    'DEFAULT_PRIORITY': 'now'
}
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'core.apps.CoreConfig',    
    'video.apps.VideoConfig',
    'instructor.apps.InstructorConfig',
    'livestream.apps.LivestreamConfig',
    'custom_user.apps.CustomUserConfig',
    'widget_tweaks',
    'tinymce',
    "post_office",

] + get_core_apps(['customer','promotions','basket','catalogue','payment','partner','order','checkout'])

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'customer.middlewares.CourseExistsMiddleware',
    'customer.middlewares.CoursePublishedMiddleware',
    'customer.middlewares.CourseEnrolledMiddleware',
    'customer.middlewares.OwnerRequiredMiddleware',
    'customer.middlewares.AnonymousRequiredMiddleware',
    'customer.middlewares.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'sosci.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                 os.path.join(BASE_DIR,'sosci','templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ],
        },
    },
]

WSGI_APPLICATION = 'sosci.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {}
DATABASES['default'] = dj_database_url.config(default=os.environ['DATABASE_URL'])

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Jamaica'

SITE_ID = 1

SITE_NAME = "sosci"

SITE_DOMAIN = "sosci.herokuapp.com"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = "d M Y"

AUTH_USER_MODEL = 'custom_user.User'

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = location("public/media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

STATIC_ROOT = location('public/static')

STATICFILES_DIRS = (
    location('sosci/static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGIN_REQUIRED_URLS = (
    r'^/catalogue/my-courses/$',
    r'^/catalogue/my-enrolled-courses/$',
    r'^/catalogue/my-created-courses/$',
    r'^/catalogue/course/create/$',
    r'^/catalogue/live/create/$'
)

LOGIN_REDIRECT_URL = reverse_lazy('catalogue:course-list')

LOGIN_URL = reverse_lazy('customer:user-login')

ANONYMOUS_REQUIRED_URLS = (
    r'^/accounts/login/$',
    r'^/accounts/registration/modal/(?P<course_id>\d+)/$',
    r'^/accounts/login/modal/(?P<course_id>\d+)/$',
    r'^/accounts/registration/$',    
    r'^/$',
)

COURSE_OWNER_REQUIRED_URLS = (
    r'^/instructor/',
)

COURSE_PUBLISHED_PUBLIC_URLS = (
r'^/instructor/publish/course/(?P<course_id>\d+)/$',
r'^/instructor/module/create/(?P<course_id>\d+)/$',
r'^/instructor/live/module/create/(?P<course_id>\d+)/$',
)


ENROLLMENT_PUBLIC_URLS = (
    r'^/accounts/registration/modal/(?P<course_id>\d+)/$',
    r'^/accounts/login/modal/(?P<course_id>\d+)/$',  
    r'^/instructor/publish/course/(?P<course_id>\d+)/$',    
    r'^/instructor/module/create/(?P<course_id>\d+)/$',
    r'^/instructor/live/module/create/(?P<course_id>\d+)/$',    
    r'^/checkout/payment-details/(?P<course_id>\d+)/$',
    r'^/checkout/thank-you/$',
    r'^/catalogue/course/details/(?P<course_id>\d+)/$',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

VIMEO_ACCESS_TOKEN = os.environ['VIMEO_ACCESS_TOKEN']

VIMEO_CREATE_VIDEO_URL = 'https://api.vimeo.com/me/videos'

VIMEO_GET_ALL_THUMBNAILS_URL = 'https://api.vimeo.com/videos/{0}/pictures'

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_API_KEY_SID = os.environ['TWILIO_API_KEY_SID']
TWILIO_API_SECRET = os.environ['TWILIO_API_SECRET']
TWILIO_REST_API_AUTH_TOKEN = os.environ['TWILIO_REST_API_AUTH_TOKEN']
TWILIO_CHAT_SERVICE_SID = os.environ['TWILIO_CHAT_SERVICE_SID']

from oscar.defaults import *
# Currency
OSCAR_DEFAULT_CURRENCY = 'USD'
OSCAR_CURRENCY_LOCALE = 'en_US'
OSCAR_CURRENCY_FORMAT = u'\xa4#,##0'
OSCAR_SHOP_NAME = 'sosci'
OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Processed', 'Cancelled',),
    'Cancelled': (),
}