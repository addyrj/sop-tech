import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django
django.setup()

from sop.models import DisplayTV, StatusTV, ProductionLineTV, MediaFile
from django.utils import timezone
from sop.middleware import _thread_locals
from django.db import close_old_connections   # ✅ FIX ADDED

import json
import paho.mqtt.client as mqtt

BROKER = "clienttest.industrysop.com"
PORT = 1883
USERNAME = "tvuser"
PASSWORD = "tvuser@100"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")

        client.subscribe("tv/+/+/completed")
        client.subscribe("tv/+/+/status")
    else:
        print("Connection failed")


def on_message(client, userdata, msg):
    close_old_connections()   # ✅ ONLY FIX

    topic = msg.topic
    payload = msg.payload.decode()
    print("TOPIC:", topic)

    try:
        parts = topic.split("/")

        client_name = parts[1]
        tv_id = int(parts[2])

        _thread_locals.CLIENT = client_name

        # ---------- STATUS ----------
        if parts[3] == "status":

            StatusTV.objects.update_or_create(
                tvid_id=tv_id,
                defaults={
                    "status": payload,
                    "updated_time": timezone.now()
                }
            )

        # ---------- COMPLETED ----------
        elif parts[3] == "completed":

            tv = DisplayTV.objects.filter(id=tv_id).first()
            if not tv:
                print("TV not found")
                return

            current_tv_line = ProductionLineTV.objects.filter(
                display_tv=tv
            ).order_by('-id').first()

            if not current_tv_line:
                print("No production line")
                return

            current_tv_line.status = "completed"
            current_tv_line.save()

            next_tv_line = ProductionLineTV.objects.filter(
                production_line=current_tv_line.production_line,
                status="pending"
            ).order_by('id').first()

            if not next_tv_line:
                print("All done ✅")
                return

            media_files = MediaFile.objects.filter(
                media_content__production_line=current_tv_line.production_line,
                media_content__display_tv=next_tv_line.display_tv
            )

            files_list = [str(f.file) for f in media_files]

            payload_data = json.dumps({
                "tvid": next_tv_line.display_tv.id,
                "production_id": current_tv_line.production_line.id,
                "downloadable": True,
                "files": files_list
            })

            topic_pub = f"tv/{client_name}/{next_tv_line.display_tv.id}/command"

            client.publish(topic_pub, payload_data, retain=True)

    except Exception as e:
        print("Error:", e)


client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

client.loop_forever()