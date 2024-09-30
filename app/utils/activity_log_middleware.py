from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
from app.models.activity_log_model import ActivityLog
from app.models.user_model import CustomToken
import json

class ActivityLoggingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if request.content_type == 'application/json':
                try:
                    request_body = request.body.decode('utf-8')
                    self._log_request_data(request, request_body)
                except (UnicodeDecodeError, AttributeError):
                    self._log_request_data(request, 'Unable to decode body')
            elif request.content_type.startswith('multipart/form-data'):
                form_data = self.extract_form_data(request)
                self._log_request_data(request, json.dumps(form_data))
            else:
                self._log_request_data(request, None)

    def extract_form_data(self, request):
        form_data = {key: value for key, value in request.POST.items()}

        file_info = [
            {
                'field_name': key,
                'name': file.name,
                'size': file.size,
                'content_type': file.content_type
            }
            for key, file in request.FILES.items()
        ]

        return {'form_data': form_data, 'file_info': file_info}

    def process_response(self, request, response):
        return response

    def _log_request_data(self, request, body):
        user_name = 'Anonymous'
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if auth_header:
            parts = auth_header.split(' ')
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token_key = parts[1]
                user = self.get_user_from_token(token_key)
                user_name = user.username if user else 'Anonymous'

        data = body if isinstance(body, str) else 'No body or binary data'

        try:
            ActivityLog.objects.create(
                table_name='N/A',
                user_name=user_name,
                action=f'{request.method} {request.path}',
                ip_address=self.get_client_ip(request),
                data=data[:1000],
                reg_date=datetime.now(),
                response_status=None,  # To be updated later if needed
                processing_time=None   # To be calculated later if needed
            )
        except Exception as e:
            # Log the exception if needed
            pass

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_user_from_token(self, token_key):
        try:
            token = CustomToken.objects.get(token_key=token_key)
            return token.user
        except CustomToken.DoesNotExist:
            return None
