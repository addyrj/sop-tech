from rest_framework import serializers
from sop.models import StatusTV, StorageTV

class TvFileGetSerializer(serializers.Serializer):
    tv_id = serializers.IntegerField()



class TvStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusTV
        fields = "__all__"

class TvStorageSerializer(serializers.ModelSerializer):

    class Meta:
        model = StorageTV
        fields = "__all__"


class TvLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    