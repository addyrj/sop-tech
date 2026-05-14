# sop/middleware.py

import threading
import os
from django.conf import settings
from django.contrib import admin

_thread_locals = threading.local()

class ClientMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        client = 'default'

        # ✅ LOGIN REQUEST
        if request.method == "POST" and request.path.startswith("/admin/login"):

            username = request.POST.get("username", "")

            if "@" in username:
                real_username, client = username.split("@", 1)

                print(real_username,client)
                post = request.POST.copy()
                post['username'] = real_username
                request._post = post

                request._client_to_set = client


            else:
                # ✅ DEFAULT LOGIN
                request._client_to_set = 'default'
                request._clear_client_cookie = True

        # ✅ NORMAL REQUEST
        elif not hasattr(request, '_client_to_set') and request.COOKIES.get('client'):
            client = request.COOKIES.get('client')

        _thread_locals.CLIENT = client
        db_config = settings.DATABASES.get(client, {})
        
        
        
        print("MIDDLEWARE DB:", client)

        # 🔥 SET HEADER BEFORE RESPONSE
        db_config = settings.DATABASES.get(client, {})
        admin.site.site_header = db_config.get('TITLE', 'Admin Panel')
        admin.site.site_title = db_config.get('TITLE', 'Admin Panel')

        response = self.get_response(request)

            
        # ✅ SET COOKIE
        if hasattr(request, '_client_to_set'):
            response.set_cookie('client', request._client_to_set)


        if request.path.startswith("/admin/login") and response.status_code == 302:
            db_name = getattr(_thread_locals, 'CLIENT', 'default')

            # ✅ upload folder
            upload_base = os.path.join(settings.BASE_DIR, "upload")
            upload_client = os.path.join(upload_base, db_name)
            os.makedirs(upload_client, exist_ok=True)

            # ✅ tvfile folder (NEW)
            tvfile_base = os.path.join(settings.BASE_DIR, "tvfile")
            tvfile_client = os.path.join(tvfile_base, db_name)
            os.makedirs(tvfile_client, exist_ok=True)

            print("UPLOAD READY:", upload_client)
            print("TVFILE READY:", tvfile_client) 


        # ✅ SET COOKIE
        if hasattr(request, '_client_to_set'):
            response.set_cookie('client', request._client_to_set)







        # ✅ CLEAR OLD COOKIE
        if hasattr(request, '_clear_client_cookie'):
            response.delete_cookie('client')

        return response


def get_current_client():
    return getattr(_thread_locals, 'CLIENT', 'default')