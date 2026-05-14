from rest_framework import status as statuss
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TvFileGetSerializer, TvStatusSerializer, TvStorageSerializer, TvLoginSerializer
from sop.models import DisplayTV, ProductionLine, MediaContent, StatusTV, StorageTV
from django.contrib.auth import authenticate
from django.utils.timezone import localtime
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from django.contrib.auth import get_user_model
from sop.middleware import get_current_client
from sop.models import ClientUserMap
from sop.middleware import _thread_locals


from django.conf import settings

def get_db_key_from_name(db_name):
    for key, config in settings.DATABASES.items():
        if config.get('NAME') == db_name:
            return key
    return 'default'

class TvFileGetSerializerView(APIView):

    def get(self, request, tv_id, format=None):


        username = request.GET.get("username")  # 👈 frontend से भेजो

        try:
            db_key = request.GET['dataid']

            mapping = ClientUserMap.objects.using('user_credential_master').get(username=username,db_name=db_key)
            db_name = mapping.db_name

            # ✅ FORCE DB SWITCH
            _thread_locals.CLIENT = db_name

            print("API DB SWITCHED TO:", db_name)

        except ClientUserMap.DoesNotExist:
            return Response({"error": "User mapping not found"}, status=400)

        display_tv_obj = DisplayTV.objects.get(id=tv_id)

        ProductionLines = ProductionLine.objects.filter(display_tv=display_tv_obj)

        active_line_list = []

        for line in ProductionLines:
            if line.active_line == 1:
                active_line_list.append(line.id)
        if active_line_list:

            active_line_obj = ProductionLine.objects.get(id=active_line_list[0])

            result = active_line_obj.media_contents.all()

           

            required_media_content_obj = []

            for item in result:
                if item.display_tv.id == tv_id:
                    required_media_content_obj.append(item.id)


            
            print("What is inside it ?", required_media_content_obj)

            response = []

            for media_content_id in required_media_content_obj:



                final_media_content_obj = MediaContent.objects.get(id=media_content_id)

                final_queryset = final_media_content_obj.files.all()

                

                for item in final_queryset:
                    
                    
                    # Get MediaContent update time
                    media_content_updated = final_media_content_obj.updated_at
                    

                    # MediaFile update time (NEW)
                    media_file_updated = item.updated_at

                    # Get VolumeTV update time
                    volume_updated = display_tv_obj.volumetv.updated_at if hasattr(display_tv_obj, "volumetv") else media_content_updated


                    # Choose the latest time
                    last_updated_time = max(media_content_updated, media_file_updated, volume_updated)

                    # Format for API
                    last_updated_formatted = localtime(last_updated_time).strftime("%d-%m-%Y %I:%M:%S %p")
                    
                    response.append(
                        {
                            "id":item.id,
                            "user":tv_id,
                            "file_uploaded":f"https://clienttest.industrysop.com/{item.file.url}",
                            "duration":final_media_content_obj.duration,
                            "sequence":item.order,
                            "volume":display_tv_obj.volumetv.volume_tv,
                            "last_updated":last_updated_formatted,
                        }
                    )

            return Response(response, status=statuss.HTTP_200_OK)
        else:
            response = {
                "Status":"Failed",
                f"{tv_id}":"this tv does not associate with active line."
            }
            return Response(response, status=statuss.HTTP_400_BAD_REQUEST) 
        



# TV Status Serializer Api

# TV Status Serializer Api




class TvStatusSerializerView(APIView):

    def post(self, request, format=None):
        serializer = TvStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tvid = serializer.validated_data['tvid']
        status = serializer.validated_data['status']

        displaytv_obj = DisplayTV.objects.get(id=tvid.id)

        # ✅ Get existing row or create new one
        status_obj, created = StatusTV.objects.get_or_create(
            tvid=displaytv_obj,
            defaults={"status": status}
        )

        # If record already existed, update it
        if not created:
            previous_updated_time = status_obj.updated_time

            StatusTV.objects.filter(id=status_obj.id).update(
                status=status,
                updated_time=timezone.now()
            )

            status_obj.refresh_from_db()

            # ✅ Time difference logic (unchanged)
            if status_obj.updated_time - previous_updated_time > timedelta(minutes=5):
                StatusTV.objects.filter(id=status_obj.id).update(status="OFFLINE")
                status_obj.refresh_from_db()

        # ✅ Prepare response
        response_serializer = TvStatusSerializer(status_obj)
        data = response_serializer.data

        data["time"] = timezone.localtime(status_obj.time).strftime(
            "%d %b %Y, %I:%M:%S %p"
        )
        data["updated_time"] = timezone.localtime(status_obj.updated_time).strftime(
            "%d %b %Y, %I:%M:%S %p"
        )

        return Response(data, status=statuss.HTTP_200_OK)

    


# TV Storage Serializer Api


class TvStorageSerializerView(APIView):

    def post(self, request, format=None):
        storage = request.data.get('storage')
        tvid = request.data.get("tvid")

        username = request.data.get("username")  # 👈 add this
        db_name = request.data.get("db_name")

        # 🔥 DB SWITCH
        try:
            mapping = ClientUserMap.objects.using('user_credential_master').get(username=username,db_name=db_name)
            _thread_locals.CLIENT = mapping.db_name   # autofoam

            print("DB SWITCHED:", mapping.db_name)

        except ClientUserMap.DoesNotExist:
            return Response({"error": "User mapping not found"}, status=400)

        # ✅ अब सही DB में save होगा
        obj, created = StorageTV.objects.update_or_create(
            tvid=DisplayTV.objects.get(id=tvid),
            defaults={'storage': storage}
        )

        response_serializer = TvStorageSerializer(obj)
        data = response_serializer.data

        if obj:
            data['time'] = localtime(obj.time).strftime("%d %b %Y, %I:%M:%S %p")
            data['updated_time'] = localtime(obj.updated_time).strftime("%d %b %Y, %I:%M:%S %p")

        return Response(
            data,
            status=statuss.HTTP_200_OK if not created else statuss.HTTP_201_CREATED
        )


# TV Login Serializer Api

class TvLoginSerializerView(APIView):

    def post(self, request, format=None):
        serializer = TvLoginSerializer(data=request.data)

        if serializer.is_valid():

            # ✅ always use validated_data
            uusername = serializer.validated_data["username"]
            upass = serializer.validated_data["password"]

            # ✅ STEP 1: fetch DB from master DB
            try:
                mapping = ClientUserMap.objects.using('user_credential_master').get(username=uusername)
                db_name = mapping.db_name
            except ClientUserMap.DoesNotExist:
                return Response({
                    "Status": "Failed",
                    "Message": "User not mapped"
                }, status=status.HTTP_401_UNAUTHORIZED)

            User = get_user_model()

            # ✅ STEP 2: fetch user from correct DB
            try:
                user = User.objects.using(db_name).get(username=uusername)
            except User.DoesNotExist:
                return Response({
                    "Status": "Failed",
                    "Message": "Invalid user"
                }, status=status.HTTP_401_UNAUTHORIZED)

            # ✅ STEP 3: password check
            if not user.check_password(upass):
                return Response({
                    "Status": "Failed",
                    "Message": "Invalid password"
                }, status=status.HTTP_401_UNAUTHORIZED)

            print("Valid user !!")

            # ✅ STEP 4: fetch related data from same DB
            tv_profile = user.displaytv_profile.using(db_name).first()

            response = {
                "Status": "Success",
                "Message": "Valid Credentials to login",
                "User": user.username,
                "TvID": tv_profile.id if tv_profile else None,
                "TvName": tv_profile.display_number if tv_profile else None,
                "db_name":db_name
            }

            return Response(response, status=status.HTTP_200_OK)

        else:
            return Response({
                "Status": "Failed",
                "Errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

