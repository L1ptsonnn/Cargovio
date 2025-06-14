from django.contrib.auth.backends import BaseBackend
from .models import Company, Carrier

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        company_id = request.session.get('company_id')
        carrier_id = request.session.get('carrier_id')
        
        if company_id:
            try:
                return Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                return None
        elif carrier_id:
            try:
                return Carrier.objects.get(id=carrier_id)
            except Carrier.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        try:
            return Company.objects.get(id=user_id)
        except Company.DoesNotExist:
            try:
                return Carrier.objects.get(id=user_id)
            except Carrier.DoesNotExist:
                return None 