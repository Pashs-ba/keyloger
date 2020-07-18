from django.urls import path

from .views import *

urlpatterns = [
    path('', GetDataWithTime.as_view(), name='data_with_time'),
    path('create-keylogger', CreateId.as_view(), name='create_keylogger')
]
