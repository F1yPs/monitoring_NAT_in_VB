from database.models import DB_user

class UserLogin():
	def fromDB(self, user_id, DB):
		self.__user=DB.objects(pk=user_id)
		if self.__user==False:
			return False
		else:
			return self

	def create(self, user):
		self.__user=user
		return self

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(DB_user.objects(email=self.__user).to_json().split(":")[2].split(", ")[0].replace('"','').replace(' ','').replace('}',''))
#		print(DB.split(":")[2].replace('}',''))
#		return self.id
#		return str(self.__user)
