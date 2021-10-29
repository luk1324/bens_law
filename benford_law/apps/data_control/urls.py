from django.urls import path

from . import views

app_name = "data_control"
urlpatterns = [
   path('ajax/postColumn', views.postColumn, name='postColumn'),
   path('ajax/getSavedSet', views.getSavedSet, name='getSavedSet'),
   path('upload', views.upload, name='upload'),
   path('history', views.history, name='history')
]

