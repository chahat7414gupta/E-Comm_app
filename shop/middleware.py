
from django.utils.deprecation import MiddlewareMixin
from .db import SessionLocal

class SQLAlchemySessionCleanupMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        try:
            SessionLocal.remove()
        finally:
            return response
