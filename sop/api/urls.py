from django.urls import path
from . import views

urlpatterns = [
    path('tvfilegetserializerapi/<int:tv_id>/', views.TvFileGetSerializerView.as_view(), name='tvfilegetserializer'),
    path('tvstatusserializerapi/', views.TvStatusSerializerView.as_view(), name='tvstatusserializerapi'),
    path('tvstorageserializerapi/', views.TvStorageSerializerView.as_view(), name='tvstorageserializerapi'),
    path('tvloginserializerapi/', views.TvLoginSerializerView.as_view(), name='tvloginserializerapi'),

]