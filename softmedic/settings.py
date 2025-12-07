from pathlib import Path
import os

# -------------------------------------------------------------------
# BASE PATH
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# SECURITY
# -------------------------------------------------------------------
SECRET_KEY = 'django-insecure-agt+)nnaeoja-=%=%7uyk_o78)wg6q!ak!7@g!31bgsopl#o-&'

DEBUG = True  # ⚠️ Cambiar a False en producción

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# -------------------------------------------------------------------
# SESSION & CSRF SECURITY
# -------------------------------------------------------------------
SESSION_COOKIE_SECURE = False             # True solo bajo HTTPS
SESSION_EXPIRE_AT_BROWSER_CLOSE = True    # Expira al cerrar el navegador
SESSION_COOKIE_AGE = 900                  # 15 minutos
CSRF_COOKIE_SECURE = False                # True solo bajo HTTPS

# -------------------------------------------------------------------
# APPLICATIONS
# -------------------------------------------------------------------
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Local apps
    'pacientes',
    'historias.apps.HistoriasConfig',   # ✅ ACTIVACIÓN DE SEÑALES
    'users',

    # Third-party apps
    'django_extensions',  # Para runscript y extensiones
    'widget_tweaks',
]

# -------------------------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Middleware personalizado: una sesión activa por usuario
    'users.middleware.OneSessionPerUserMiddleware',
]

# -------------------------------------------------------------------
# URLS / WSGI
# -------------------------------------------------------------------
ROOT_URLCONF = 'softmedic.urls'
WSGI_APPLICATION = 'softmedic.wsgi.application'

# -------------------------------------------------------------------
# TEMPLATES
# -------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'softmedic' / 'templates'],
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

# -------------------------------------------------------------------
# DATABASE
# -------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -------------------------------------------------------------------
# PASSWORD VALIDATION
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------------------------
# INTERNATIONALIZATION
# -------------------------------------------------------------------
LANGUAGE_CODE = 'es-co'  # Español (Colombia)
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# STATIC FILES
# -------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# -------------------------------------------------------------------
# MEDIA FILES
# -------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -------------------------------------------------------------------
# DEFAULT PRIMARY KEY TYPE
# -------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------------------
# CUSTOM USER MODEL
# -------------------------------------------------------------------
AUTH_USER_MODEL = 'users.CustomUser'

# -------------------------------------------------------------------
# EMAIL CONFIGURATION PARA DESARROLLO
# -------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'Soft-Medic <no-reply@softmedic.com>'

# -------------------------------------------------------------------
# LOGGING CONFIGURATION
# -------------------------------------------------------------------
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} [{name}] {module} - {message}',
            'style': '{',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file_users': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'users.log'),
            'formatter': 'verbose',
        },
        'file_security': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'security.log'),
            'formatter': 'verbose',
        },
        'file_audit': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'audit.log'),
            'formatter': 'verbose',
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'errors.log'),
            'formatter': 'verbose',
        },
    },

    'loggers': {
        'users': {
            'handlers': ['file_users', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'security': {
            'handlers': ['file_security', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'audit': {
            'handlers': ['file_audit', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file_errors', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# -------------------------------------------------------------------
# AUTENTICACIÓN Y REDIRECCIONES
# -------------------------------------------------------------------
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/users/admin_dashboard/'
LOGOUT_REDIRECT_URL = '/users/login/'
