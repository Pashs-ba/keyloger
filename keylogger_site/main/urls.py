from django.urls import path

from .views import *

urlpatterns = [
    path('', GetAllData.as_view(), name='data_with_time'),
    path('create-keylogger', CreateId.as_view(), name='create_keylogger'),
    path('<pk>', GetDataById.as_view())
]

