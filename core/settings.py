from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-co1vt!k*hpo=403ee92^#ia1f8#t1trxe2a2p9q6!f2#gecgpg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['clienttest.industrysop.com','industrysop.com','127.0.0.1']


CSRF_TRUSTED_ORIGINS = [
    "https://clienttest.industrysop.com",
    "http://clienttest.industrysop.com",   # 👈 add this
]

# Application definition

INSTALLED_APPS = [
    "jazzmin",      
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'sop',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',    
    'django.middleware.csrf.CsrfViewMiddleware',
    'sop.middleware.ClientMiddleware', 
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


DATABASE_ROUTERS = ['sop.db_router.ClientRouter']

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'sop/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sop.context_processors.dashboard_text',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

        




AUTHENTICATION_BACKENDS = [
    'sop.backends.MultiDBAuthBackend',
]




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'clienttest',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
        'TITLE': 'Iottech Administration',
    },

    'user_credential_master': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'user_credential_master',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
        'TITLE': 'Micromatic Admin'
    }

}




# AUTHENTICATION_BACKENDS = [
#     'sop.backends.CheckSubscription',  # Our custom backend first
# ]



# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.mysql',
#          'NAME': 'taxinq_sop_data_testing',
#          'USER': 'taxinq_sop_data_testing',
#          'PASSWORD': 'taxinq_sop_data_testing',
#          'HOST': 'localhost',
#          'PORT': '3306',
#          'OPTIONS': {
#              'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
#          }
#      }
#  }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

TIME_ZONE = "Asia/Kolkata"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = '/staticfiles/'

STATIC_ROOT = BASE_DIR / 'staticfiles' 


JAZZMIN_UI_TWEAKS = {
    "fonts": {
        "base_font_family": "Arial, sans-serif",
        "heading_font_family": "Arial, sans-serif",
    }
}



# settings.py
DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 500 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 500 MB

# Media path set directly to upload folder
MEDIA_URL = '/'
MEDIA_ROOT = BASE_DIR

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#--------------jazzmin settings admin panel

JAZZMIN_SETTINGS = {
    "site_title": "My Admin",
    "site_header": "My Project Admin",
    "welcome_sign": "Welcome to Ambrane Admin Panel",
    "custom_dashboard_template": "admin/index.html",  # ✅ here
}





