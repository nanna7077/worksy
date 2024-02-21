import os
from waitress import serve
from app import app
serve(app, port=os.getenv("PORT", 5000))