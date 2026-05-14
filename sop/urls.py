from django.urls import path
from . import views

urlpatterns = [
    path("update-order/", views.update_order, name="update-order"),
    path('mediabucket/select/', views.select_folders, name='media_bucket_select'),
    path('mediabucket/select/files_ajax/', views.select_files_ajax, name='media_bucket_files'),


    path("user/api/deletemultple/",views.delete_multiple_view),
    path('update-name/', views.update_name_api, name='update_name_api'),
    path('publish/', views.publishs, name='publishs'),
    path("delete_content/",views.delete_content,name="delete_content"),
    path("update_folder/",views.update_folder_view,name="update_folder_view"),
    path("change_duration/",views.change_duration),
    path("tv-download-status/<int:production_id>/", views.tv_download_status,name="tv_download_status"),
    path("upload-media/", views.upload_media_bucket, name="upload_media_bucket"),
    path("update_sequence/", views.update_sequence, name="update_sequence"),
    path('upload_image/', views.upload_image, name='upload_image'),


]
