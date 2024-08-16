from rest_framework import serializers
from . models import UrlShortner

class ShortUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model : UrlShortner
        fields = ('long_url','alias')