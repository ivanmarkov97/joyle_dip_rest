from main_app.api.views import MainDetail
from delegate_app.models import Delegation
from delegate_app.api.serializers import DelegateSerializer

class DelegateDetail(MainDetail):
	model_type = Delegation
	model_serializer = DelegateSerializer
	