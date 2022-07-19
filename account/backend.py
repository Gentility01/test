from django.contrib.auth import get_user_model 
from django.contrib.auth.backends import ModelBackend, UserModel


#GO TO THE SETTINGS.PY AND COMPLETE THE SETTINGS

class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs ):
        UserModel = get_user_model()  #getting usermoels from settings.py(line 30)
        if username is None:
            username=kwargs.get(UserModel.USERNAME_FIELD) # USERNAME_FIELD FROM THE MODELS (line 77) 


        try:
            case_insensitve_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            user = UserModel._default_manager.get(**{case_insensitve_username_field: username})
        except UserModel.DoesNotExist:
            UserModel().set_password(password)  
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

  