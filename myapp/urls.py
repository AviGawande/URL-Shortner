from django.urls import path,include
from . import views

urlpatterns = [
    path('shorten',views.short_url,name='short_url'),
    path('delete/<str:alias>',views.delete_alias,name='delete_alias'),
    path('<str:alias>/',views.redirect_to_long_url,name='redirect_to_long_url'),
    
]