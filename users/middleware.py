# users/middleware.py
from django.contrib.auth import logout
from django.contrib.sessions.models import Session

class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_session_key = request.session.session_key
            active_sessions = Session.objects.filter(expire_date__gt=request.session.get_expiry_date())
            for session in active_sessions:
                data = session.get_decoded()
                if data.get('_auth_user_id') == str(request.user.id) and session.session_key != current_session_key:
                    session.delete()  # Elimina otras sesiones activas
        return self.get_response(request)
