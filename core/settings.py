from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-secret-key'

DEBUG = True

ALLOWED_HOSTS = ['*','10.36.83.65', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    "jazzmin",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',

    'rest_framework',
    'employees',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
JAZZMIN_SETTINGS = {

    "site_title": "GVPR Admin",

    "site_header": "GVPR Employee System",

    "site_brand": "GVPR",
    
    "site_logo": "img/gvpr-logo.png",

    "login_logo": "img/gvpr-logo.png",

    "site_logo_classes": "img-fluid gvpr-admin-logo" ,

    "welcome_sign": "Welcome To GVPR Employee Management",

    "copyright": "GVPR Engineers Ltd",

    "search_model": "employees.Employee",

    "topmenu_links": [

        {"name": "Admin Dashboard", "url": "admin:index"},
        {"name": "Main Website", "url": "dashboard", "new_window": False},
        {"name": "Reports", "url": "reports", "permissions": ["employees.export_employee_excel"]},

    ],

    "icons": {

        "employees.Employee": "fas fa-users",
        "employees.EmployeeDocument": "fas fa-file",

    },

    "show_sidebar": True,

    "navigation_expanded": True,

    "hide_apps": [],

    "hide_models": [],

    "order_with_respect_to": [

        "employees",

    ],

    "custom_css": "css/gvpr-admin.css",

    "custom_js": None,

}

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'employees.context_processors.employee_notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mine_qr_system',
        'USER': 'root',
        'PASSWORD': 'Suman@123',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True
