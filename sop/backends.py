# sop/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .middleware import get_current_client

UserModel = get_user_model()

class MultiDBAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        db = get_current_client()
        print("AUTH DB:", db)

        if username is None or password is None:
            return None

        # 🔥 try selected DB
        try:
            user = UserModel.objects.using(db).get(username=username)
        except UserModel.DoesNotExist:

            # ✅ fallback to default
            if db != 'default':
                try:
                    user = UserModel.objects.using('default').get(username=username)
                    db = 'default'
                    print("FALLBACK TO DEFAULT")
                except UserModel.DoesNotExist:
                    return None
            else:
                return None

        if user.check_password(password):
            return user

        return None