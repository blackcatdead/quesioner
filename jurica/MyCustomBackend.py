from jurica.models import Responden
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class MyCustomBackend:
	def authenticate(self, email=None):
		try:
			responden = Responden.objects.get(email=email)
			if responden:
				if not responden.status == 0:
					return responden
				else:
					return None
			else:
				return None
		except Responden.DoesNotExist:
			return None

	def get_responden(self, id):
		try:
			return Responden.objects.get(id_responden=id)
		except Responden.DoesNotExist:
			return None

	def authenticateadmin(self, uname, password):
		try:
			if uname == 'admin' and password == 'admin':
				return True
			else:
				return False
		except Exception as e:
			return False
