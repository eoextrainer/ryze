from app_server import app

# Enable mobile-only rendering for templates
app.config["MOBILE_ONLY"] = True

# Expose a simple run entry (used by Gunicorn)
# gunicorn app_mobile_server:app -b 0.0.0.0:8001 --workers 1
