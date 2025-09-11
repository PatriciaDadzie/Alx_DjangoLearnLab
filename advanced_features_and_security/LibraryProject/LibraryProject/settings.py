from pathlib import Path 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e4=75ab@_$$qkq!nka8nsqpp(_=5zhike0c(@wx78$v+qnvl^o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # Turn off in production

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CSP Middleware for Content Security Policy
    'csp',

    # Custom apps
    'bookshelf',
    'relationship_app',
]

MIDDLEWARE = [
    'csp.middleware.CSPMiddleware',  # CSP Middleware to add Content-Security-Policy headers
    'django.middleware.security.SecurityMiddleware',  # Security enhancements like SSL redirect
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Prevent clickjacking
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# === SECURITY SETTINGS ===

# Enable browser XSS filter and prevent rendering if an attack is detected
SECURE_BROWSER_XSS_FILTER = True

# Prevent site from being rendered inside an iframe to avoid clickjacking
X_FRAME_OPTIONS = 'DENY'

# Prevent MIME type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True  # Enforce HTTPS in production

# Trust the proxy/load balancer header for detecting HTTPS requests
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HTTP Strict Transport Security (HSTS) settings
SECURE_HSTS_SECONDS = 31536000  # Cache HSTS for 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply HSTS to all subdomains
SECURE_HSTS_PRELOAD = True  # Allow domain to be included in browser preload list

# Cookies will only be sent over HTTPS connections
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# === CONTENT SECURITY POLICY (CSP) SETTINGS ===

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", 'https://cdnjs.cloudflare.com')
CSP_STYLE_SRC = ("'self'", 'https://fonts.googleapis.com')
CSP_FONT_SRC = ("'self'", 'https://fonts.gstatic.com')
CSP_IMG_SRC = ("'self'", 'data:')  # Allow images from self and base64 encoded images
CSP_CONNECT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
