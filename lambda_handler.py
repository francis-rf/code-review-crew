"""
AWS Lambda handler for Code Review Crew FastAPI application
"""
from mangum import Mangum
from app import app

# Create Lambda handler
handler = Mangum(app)
