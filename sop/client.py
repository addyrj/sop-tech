# import paho.mqtt.publish as publish
# import json

# def send_tv_command(tv_topic, media_url):

#     payload = {
#         "action": "play_media",
#         "media_url": media_url
#     }

#     publish.single(
#         tv_topic,
#         json.dumps(payload),
#         hostname="192.168.1.3",
#         port=1883
#     )