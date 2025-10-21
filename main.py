"""
Main entry point for Google App Engine.
This file is required for App Engine to detect the application.
"""
from photography_config.wsgi import application

# App Engine uses this application object
app = application
