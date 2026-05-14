from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.views.decorators.clickjacking import xframe_options_exempt
import json
from django.db import transaction
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status as statuss
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import TvFileGetSerializer, TvStatusSerializer, TvStorageSerializer, TvLoginSerializer
from .models import DisplayTV, ProductionLine, MediaContent, StatusTV, StorageTV
from django.contrib.auth import authenticate
from django.utils.timezone import localtime
from datetime import timedelta, datetime
import paho.mqtt.client as mqtt
from sop.middleware import get_current_client


import shutil
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MediaBucket


BROKER = "clienttest.industrysop.com"
PORT = 1883
USERNAME = "tvuser"
PASSWORD = "tvuser@100"

class TvFileGetSerializerView(APIView):

    def get(self, request, tv_id, format=None):

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
                            "file_uploaded":f"http://192.168.1.3:8000{item.file.url}",
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

from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response

class TvStatusSerializerView(APIView):

    def post(self, request, format=None):
        serializer = TvStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tvid = serializer.validated_data['tvid']
        status = serializer.validated_data['status']

        displaytv_obj = DisplayTV.objects.get(id=tvid.id)

        # âœ… Get existing row or create new one
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

            # âœ… Time difference logic (unchanged)
            if status_obj.updated_time - previous_updated_time > timedelta(minutes=5):
                StatusTV.objects.filter(id=status_obj.id).update(status="OFFLINE")
                status_obj.refresh_from_db()

        # âœ… Prepare response
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
        serializer = TvStorageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tvid = serializer.validated_data['tvid']
        storage = serializer.validated_data['storage']

        obj, created = StorageTV.objects.update_or_create(
            tvid=tvid,
            defaults={'storage': storage}
        )

        response_serializer = TvStorageSerializer(obj)
        data = response_serializer.data

        # format datetime here
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
            uusername = serializer.data["username"]
            upass = serializer.data["password"]
            user = authenticate(username=uusername,password=upass)
            if user !=None:
                print("Valid user !!")

                response = {
                    "Status":"Success",
                    "Message":"Valid Credentials to login",
                    "User":user.username,
                    "TvID":user.displaytv_profile.id,
                    "TvName":user.displaytv_profile.display_number,
                }
                return Response(response, status=statuss.HTTP_200_OK)
            else:
                response = {
                    "Status":"Failed",
                    "Message":"Invalid Credentials",
                    "phone":uusername,
                    "password":upass,
                }
                return Response(response, status=statuss.HTTP_401_UNAUTHORIZED)
        else:
            response = {"Status":"Failed","Errors":serializer.errors}
            return Response(response, status=statuss.HTTP_400_BAD_REQUEST)


@csrf_exempt
def delete_multiple_view(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        ids_str = body.split("=")[1]
        ids_list = [int(i) for i in ids_str.split(",")]
        qs = MediaFile.objects.filter(id__in=ids_list)

        media_content_ids = list(qs.values_list('media_content_id', flat=True))
        qs.delete()
        
        for mc_id in set(media_content_ids):

            remaining = MediaFile.objects.filter(
                media_content_id=mc_id
            ).count()

            print(f"MediaContent {mc_id} remaining files:", remaining)

            if remaining == 0:
                print(f"Deleting MediaContent {mc_id}")

                MediaContent.objects.filter(
                    id=mc_id
                ).delete()

        return JsonResponse({"status": "success", "deleted_ids": ids_list})


def update_order(request):
    if request.method == "POST":
        file_id = request.POST.get("id")
        new_order = request.POST.get("value")
        try:
            obj = MediaFile.objects.get(id=file_id)
            obj.order = int(new_order)
            obj.save()
            return JsonResponse({"status": "success"})
        except MediaFile.DoesNotExist:
            return JsonResponse({"status": "error", "message": "File not found"})
    return JsonResponse({"status": "invalid"})


@xframe_options_exempt
def select_folders(request):
    folders = MediaBucket.objects.values('folder_name').annotate(file_count=Count('id')).order_by('folder_name')
    return render(request, "admin/sop/mediabucket/modall_folders.html", {
        "folders": folders
    })

@xframe_options_exempt
def select_files_ajax(request):
    folder_name = request.GET.get("folder_name")
    files = MediaBucket.objects.filter(folder_name=folder_name)

    # Serialize files for JS
    data = []
    for f in files:
        data.append({
            "id": f.id,
            "filename": f.file.name.split("/")[-1],
            "url": f.file.url,
            "is_image": f.file.name.lower().endswith((".jpg", ".png", ".jpeg", ".webp")),
            "is_video": f.file.name.lower().endswith((".mp4", ".mov", ".avi"))
        })

    return JsonResponse({"files": data})




@csrf_exempt  # Agar CSRF token handle kar rahe ho, ye optional
def update_name_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            obj_id = data.get("id")
            new_name = data.get("name")

            obj = DisplayTV.objects.get(id=obj_id)
            obj.display_number = new_name
            obj.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid method"})























def publishs(request):
    if request.method != "POST":
        return JsonResponse({"status": "Failed", "message": "Method Not allowed"})

    data = json.loads(request.body)
    get_production_id = data.get("production_id")
    get_bucket_id = data.get("bucket_id")
    duration = data.get("duration")
    media_system_id = data.get("media_system_id")

    # Fetch production line and TVs in order
    production_instance = get_object_or_404(ProductionLine, id=get_production_id)
    
    # tv_list = list(production_instance.display_tv.all().order_by("id"))  # sequence order: Tv2, Tv4, Tv6, Tv7
    tv_ids = json.loads(production_instance.tv_order)

    # fetch TVs
    tv_list = list(DisplayTV.objects.filter(id__in=tv_ids))

    # 🔥 order maintain
    tv_list.sort(key=lambda x: tv_ids.index(str(x.id)))
    updater = request.session.get("update_duration",[])
    duration_map = {str(i['file_id']): int(i["duration"]) for i in updater}
    
    # Collect media files from the selected bucket
    media_bucket = []
    buckets = MediaBucket.objects.filter(id=get_bucket_id)
    for b in buckets:
        bucket_items = MediaBucket.objects.filter(folder_name=b.folder_name).order_by("sequence")
        for u in bucket_items:
            media_bucket.append(u.file)


    # Set up MQTT client
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)
    client.connect(BROKER, PORT, 60)

    # Loop through each TV and send MQTT message
    for i, tv in enumerate(tv_list):

        # Only the first TV in sequence gets ok_to_download=True
        downloadable = True if i == 0 else False

        # Filter media files for this TV
        files_for_tv = [f for f in media_bucket if tv.display_number in str(f)]
        # Prepare payload
        payload = json.dumps({
            "tvid": tv.id,
            "production_id": get_production_id,
            "downloadable": downloadable,
            "files": [str(f) for f in files_for_tv]
        })

        # Dynamic topic per TV
        topic = f"tv/{tv.id}/command"
        client.publish(topic, payload,retain=True)
        
        # Create MediaContent / MediaFile entries
        for file_obj in files_for_tv:

            
            # Determine duration: session update or default
            
            file_duration = duration_map.get(file_obj.name, duration)
            
            media_content_obj, created = MediaContent.objects.get_or_create(
                production_line=production_instance,
                display_tv=tv,
                defaults={'duration': int(file_duration)},
                filename=file_obj.name,
                is_published=True
            )

            MediaFile.objects.get_or_create(media_content=media_content_obj, file=file_obj)

        # Set default TV volume
        VolumeTV.objects.update_or_create(displaytv=tv, defaults={'volume_tv': 50})

    # Disconnect MQTT client after sending to all TVs
    client.disconnect()

    # Mark media system as published
    handle = get_object_or_404(MediaSystem, id=media_system_id)
    handle.is_published = True
    handle.save()
    try:
        del request.session['update_duration']
    except Exception as error:
        pass
    return JsonResponse({
        "status": "success",
        "message": f"Published to {len(tv_list)} TVs successfully. First TV is ready to download."
    })


class TvDeleteData(APIView):

    def post(self, request, tv_id, format=None):
        pass





def delete_content(request):
    if request.method == "POST":
        data = json.loads(request.body)

        production_id = data.get("production_id")
        media_system_id = data.get("media_system_id")

        production_instance = get_object_or_404(
            ProductionLine,
            id=production_id
        )

        # ðŸ”¥ Delete all media files linked to this production
        media_contents = MediaContent.objects.filter(
            production_line=production_instance
        )

        # Delete related MediaFile first (safe way)
        MediaFile.objects.filter(media_content__in=media_contents).delete()

        # Delete MediaContent
        media_contents.delete()

        # Update MediaSystem
        handle = MediaSystem.objects.get(id=media_system_id)
        handle.is_published = False
        handle.save()

        return JsonResponse({"status": "OK", "message": "Unpublished & Deleted"})

    return JsonResponse({"status": "Failed", "message": "Method Not allowed"})


# In MediaBucketAdmin
@csrf_exempt
def update_folder_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for item in data.get('order', []):
            MediaBucket.objects.filter(id=item['id']).update(sequence=item['sequence'])
        return JsonResponse({'status': 'success'})



@csrf_exempt
def change_duration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            file_id = data.get("file_id")
            duration = data.get("duration")
            media_system_id = data.get("media_system_id")
            production_id = data.get("production_id")

            if not file_id:
                return JsonResponse({"status": "ERROR", "msg": "file_id missing"})

            # ✅ get existing OR empty
            session_data = request.session.get("update_duration", [])

            # ✅ FULL CLEAN duplicate + invalid
            cleaned_data = {}
            for i in session_data:
                if i.get("file_id"):
                    cleaned_data[str(i["file_id"])] = i

            # ✅ update / insert current
            cleaned_data[str(file_id)] = {
                "file_id": file_id,
                "duration": duration,
                "media_system_id": media_system_id,
                "production_id": production_id
            }

            # ✅ convert back to list
            request.session["update_duration"] = list(cleaned_data.values())
            request.session.modified = True

            print("SESSION:", request.session["update_duration"])

            return JsonResponse({
                "status": "OK",
                "msg": request.session["update_duration"]
            })

        except Exception as e:
            return JsonResponse({"status": "ERROR", "msg": str(e)})

    return JsonResponse({"status": "FAILED"})
    

def tv_download_status(request, production_id):
    if request.method == "GET":
        tvs = ProductionLineTV.objects.filter(production_line_id=production_id)

        completed = tvs.filter(status="completed").count()
        total = tvs.count()

        tv_list = []

        for tv in tvs:
            tv_list.append({
                "tv_id": tv.display_tv.id,
                "tv_name": tv.display_tv.display_number,
                "status": tv.status
            })

        return JsonResponse({
            "completed": completed,
            "total": total,
            "tvs": tv_list
        })







import os
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import MediaBucket, DisplayTV

@csrf_exempt
def upload_media_bucket(request):
    if request.method == "POST":
        folder_name = request.POST.get("folder_name")

        if not folder_name:
            return JsonResponse({"status": "error", "message": "Folder name required"})

        folder_name = folder_name.strip().lower()

        files = request.FILES.getlist("files")

        # ✅ STORAGE LIMIT CHECK (based on TVs)
        tv_count = DisplayTV.objects.count()
        total_limit = tv_count * 1024**3  # 1GB per TV

        # ✅ CURRENT USED STORAGE
        media_files = MediaBucket.objects.filter(created_by=request.user)
        used_size = 0

        for media in media_files:
            if media.file:
                file_path = os.path.join(settings.MEDIA_ROOT, str(media.file))
                if os.path.exists(file_path):
                    used_size += os.path.getsize(file_path)

        # ✅ NEW UPLOAD SIZE
        upload_size = sum(f.size for f in files)
        db_name = get_current_client()
        # ❌ BLOCK IF LIMIT EXCEEDED
        if used_size + upload_size > total_limit:
            return JsonResponse({
                "status": "error",
                "message": f"Storage Full! Used {(used_size/(1024**3)):.2f} GB / {tv_count} GB"
            })


        folder_path = os.path.join(settings.MEDIA_ROOT,"upload",db_name,folder_name)


        # 🔥 delete old folder (your original logic unchanged)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)

        sequence = 1

        for f in files:
            file_path = os.path.join(folder_path, f.name)

            # save file manually
            with open(file_path, "wb+") as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

            # save DB
            MediaBucket.objects.create(
                file=f"upload/{db_name}/{folder_name}/{f.name}",
                folder_name=folder_name,
                sequence=sequence,
                created_by=request.user
            )

            sequence += 1

        return JsonResponse({
            "status": "success",
            "message": "Files uploaded successfully"
        })

    return JsonResponse({"status": "error", "message": "Invalid request"})




@csrf_exempt  # optional (agar CSRF already handle kar rahe ho to hata sakte ho)
def update_sequence(request):
    if request.method != "POST":
        return JsonResponse({"status": "FAILED", "message": "Invalid method"})

    try:
        data = json.loads(request.body)
        order = data.get("order", [])


        for item in order:
            MediaBucket.objects.filter(id=item["id"]).update(
                sequence=item["sequence"]
            )

        return JsonResponse({"status": "OK"})

    except Exception as e:

        return JsonResponse({
            "status": "FAILED",
            "message": str(e)
        })





def upload_image(request):
    if request.method == "POST":
        print("Called")

        # 'image' key wahi hai jo FormData me append kiya tha
        uploaded_files = request.FILES.getlist('images')
        production_id = request.POST.get("production_id")
        display_tv = request.POST.get("tvname")
        duration = request.POST.get("duration")

        formats = (".mp3",".mp4",".mpeg",".vlc",".mov")

        if not uploaded_files:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        # Image ko media folder me save karna

        folder = MediaSystem.objects.get(production_line=production_id).select_folder.folder_name
        production_line = ProductionLine.objects.get(id=production_id)
        tv = DisplayTV.objects.get(display_number=display_tv.strip())

        project_root = settings.BASE_DIR  # BASE_DIR usually project root
        client  = get_current_client()
        upload_dir = os.path.join(project_root, "tvfile", client)

        for uploaded_file in uploaded_files:
            file_path = os.path.join(upload_dir, uploaded_file.name)

            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        

            media_content = MediaContent.objects.filter(
                display_tv=tv,
                production_line=production_line
            ).first()

    
            if not media_content:
                # create new if none exist
                media_content = MediaContent.objects.create(
                    display_tv=tv,
                    production_line=production_line,
                    duration=duration if not uploaded_file.name.lower().endswith(formats) else 0,
                    is_published=True,
                    filename=uploaded_file.name
                )
            else:


                media_content = MediaContent.objects.create(
                    display_tv=tv,
                    production_line=production_line,
                    duration=duration if not uploaded_file.name.lower().endswith(formats) else 0,
                    is_published=True,
                    filename=uploaded_file.name
                )
            media_file, mf_created = MediaFile.objects.update_or_create(
                media_content=media_content,
                file=f"tvfile/{client}/{uploaded_file.name}",   # 👈 FIX
                defaults={"order": "auto"}
            )

        VolumeTV.objects.get_or_create(
            displaytv=tv,
            defaults={'volume_tv': 0}
        )



        return JsonResponse({
            "message": "Upload successful",
            "filename": uploaded_file.name
        })

    return JsonResponse({"error": "Invalid request"}, status=400)
