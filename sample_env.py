import os

# Load environment variables for local development
# Uncomment and adjust as necessary for local development
"""
os.environ['DEV'] = '1'
os.environ['ALLOWED_HOST'] = 'http://localhost:8000/' # Api server
os.environ['CLIENT_ORIGIN_DEV'] = 'http://localhost:5173'  # Frontend application server
"""

# Load environment variables for production deployment
# Uncomment and adjust as necessary for production deployment
"""
os.environ['DATABASE_URL'] = "postgres://uwc..."  # Database URL for production
os.environ.setdefault("SECRET_KEY", "...")  # Secret key for Django application
os.environ.setdefault("ALLOWED_HOST", "social-media.herokuapp.com/")  # Allowed host for production
os.environ.setdefault("CLOUDINARY_URL", "cloudinary://18...")  # Cloudinary configuration URL
"""
