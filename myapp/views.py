import time  
import random
import string
from rest_framework import status 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,HttpResponseNotFound


url_map = {}

DEFAULT_TTL = 120
SHORT_URL_PREFIX = "https://short.ly/"

def generate_random_alias(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def check_alias_expired(alias):
    if alias not in url_map:
        return True
    creation_time , ttl = url_map[alias]["creation_time"],url_map[alias]["ttl"]
    return (time.time() - creation_time) > ttl

def clean_expired_aliases():
    expired_aliases = [alias for alias in url_map if check_alias_expired(alias)]
    for alias in expired_aliases:
        del url_map[alias]

@api_view(['POST'])
def short_url(request):
    data = request.data
    long_url = data.get("long_url")
    custom_alias = data.get("custom_alias")
    ttl = data.get("ttl_seconds",DEFAULT_TTL)

    if not long_url:
        return Response({"error": "Long URL is Needed!"},status=status.HTTP_400_BAD_REQUEST)
    
    alias = custom_alias or generate_random_alias()
    while alias in url_map:
        alias = generate_random_alias()

    url_map[alias] = {
        "long_url":long_url,
        "ttl": ttl,
        "creation_time":time.time()
    }

    short_url = SHORT_URL_PREFIX + alias
    return Response({"short_url":short_url},status=status.HTTP_201_CREATED)

@api_view(['GET'])
def redirect_to_long_url(request,alias):
    clean_expired_aliases()

    if alias not in url_map or check_alias_expired(alias):
        return Response({"error":"Alias does not exist or is expired"},status=status.HTTP_404_NOT_FOUND)
    
    url_map[alias].setdefault("access_count",0)
    url_map[alias]["access_count"] += 1
    url_map[alias].setdefault("access_times",[])
    url_map[alias]["access_times"].append(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))

    long_url = url_map[alias]["long_url"]
    return HttpResponseRedirect(long_url)
    


@api_view(['GET'])
def get_analytics(request,alias):
    clean_expired_aliases()

    if alias not in url_map or check_alias_expired(alias):
        return Response({"error":"Alias does not exist or is expired"},status=status.HTTP_404_NOT_FOUND)
    
    url_data = url_map[alias]
    access_times = access_times_map[alias][-10:]
    return Response({
        "alias":alias,
        "long_url":url_data["long_url"],
        "access_count":url_data["access_count"],
        "access_times":access_times,
    })

@api_view(['DELETE'])
def delete_alias(request,alias):
    clean_expired_aliases()

    if alias not in url_map or check_alias_expired(alias):
        return Response({"error":"Alias does not exist or is expired"},status=status.HTTP_404_NOT_FOUND)
    
    del url_map[alias]
    
    return Response({"message":"Successfully deleted"},status=status.HTTP_200_OK)

    
    






