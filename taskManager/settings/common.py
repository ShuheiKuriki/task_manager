"""
Django settings for taskManager project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',                         #追加
    'allauth',                                      #追加
    'allauth.account',                              #追加
    'allauth.socialaccount',                        #追加
    # 'allauth.socialaccount.providers.line',
    'taskManager',
    'bootstrap4',
    'macros',
    'accounts.apps.AccountsConfig',
    'notify.apps.NotifyConfig',
    'task.apps.TaskConfig',
    'book.apps.BookConfig',
    'shoppinglist.apps.ShoppinglistConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'taskManager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {}

WSGI_APPLICATION = 'taskManager.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# LOGIN_URL='/'
# LOGOUT_REDIRECT_URL = '/'

# Don't forget this little dude.
SITE_ID = 1

# ログインのリダイレクトURL
# LOGIN_REDIRECT_URL = '/accounts/'
#
# # ログアウトのリダイレクトURL
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
#
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True #ユーザー登録画⾯で必須項⽬に
ACCOUNT_EMAIL_VERIFICATION = 'none'


AUTHENTICATION_BACKENDS = (
    # 'djago.contrib.auth.backends.ModelBackend',
    "allauth.account.auth_backends.AuthenticationBackend",
)

#認証⽅式を 「メールアドレスとパスワード」 に変更
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = True

# EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
#
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'apikey'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS= [
    os.path.join(BASE_DIR, "static")
]
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Don't forget this little dude.
# SITE_ID = 1
#
# # ログインのリダイレクトURL
# LOGIN_REDIRECT_URL = '/'
#
# # ログアウトのリダイレクトURL
# ACCOUNT_LOGOUT_REDIRECT_URL = '/'
#
# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
#     "allauth.account.auth_backends.AuthenticationBackend",
# )
#
# SOCIALACCOUNT_PROVIDERS = {
#     'line': {
#         'SCOPE': ['profile','openid'],
#     }
# }
