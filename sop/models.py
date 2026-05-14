from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
import subprocess
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from sop.middleware import get_current_client


def tvfile_upload_path(instance, filename):
    db = get_current_client()   # 👈 middleware से मिलेगा
    return f"tvfile/{db}/{filename}"

class BaseAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='%(class)s_profile')
    admin_username = models.CharField(max_length=150, null=True, blank=True)
    admin_password = models.CharField(max_length=150, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_%(class)ss')

    class Meta:
        abstract = True



class Admin(BaseAdmin):
    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"


class ProductionAdmin(BaseAdmin):
    class Meta:
        verbose_name = "Production Admin"
        verbose_name_plural = "User"


    def __str__(self):
        return self.admin_username


class DisplayTV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="displaytv_profile")
    display_number = models.CharField(max_length=100)



    def __str__(self):
        return self.display_number
    

class ProductionLine(models.Model):
    productionline_name = models.CharField(max_length=100)
    # description = models.CharField(max_length=100, default="Assembly Department")
    description = models.TextField()
    display_tv = models.ManyToManyField(DisplayTV)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='userinfo')
    active_line = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tv_order = models.TextField(blank=True, null=True)  # ✅ ADD THIS


    

    
    def delete(self, *args, **kwargs):
        # 🔥 yaha tera logic chalega
        print(f"Deleted Production Line: {self.productionline_name}")


        super().delete(*args, **kwargs)
    
    def associated_tvs(self):
        return " , ".join([str(i) for i in self.display_tv.all()])
    
    def __str__(self):
        return self.productionline_name


class MediaContent(models.Model):

    production_line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE, related_name="media_contents", verbose_name="Select Production Line")
    display_tv = models.ForeignKey(DisplayTV, on_delete=models.CASCADE, related_name="media_contents", verbose_name="Select TV")
    duration = models.IntegerField(default=0)
    filename = models.CharField(max_length=100, null=True,default='')
    is_published = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self):
        return f"{self.display_tv}"
    

    class Meta:
        verbose_name = "Media Content"
        verbose_name_plural = "Display"



    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.display_tv:
            VolumeTV.objects.get_or_create(
                displaytv=self.display_tv,
                defaults={'volume_tv': 0}
            )


class MediaFile(models.Model):

    media_content = models.ForeignKey(MediaContent, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=tvfile_upload_path)
    order = models.CharField(max_length=50, default="auto")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)



    class Meta:
            ordering = ['order']

    def __str__(self):
        return self.file.name


    def save(self, *args, **kwargs):
        print("Calledmediafile")
        super().save(*args, **kwargs)


        # 🔹 Set filename in parent MediaContent (latest uploaded file)
        if self.file and self.media_content:
            self.media_content.filename = os.path.basename(self.file.name)
            self.media_content.save(update_fields=['filename'])



def media_upload_path(instance, filename):
    db = get_current_client()

    if instance.folder_name:
        folder = instance.folder_name.strip().lower()
        return f"upload/{db}/{folder}/{filename}"

    return f"upload/{db}/{filename}"

class MediaBucket(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to=media_upload_path)
    folder_name = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    sequence = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return self.folder_name
        
    def save(self, *args, **kwargs):
        if self.folder_name:
            self.folder_name = self.folder_name.strip().lower()
        super().save(*args, **kwargs)
    

class StatusTV(models.Model):
    tvid = models.ForeignKey(DisplayTV, on_delete=models.CASCADE, null=True, blank=True, related_name="status_tvs", verbose_name="Display")
    status = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True, verbose_name="Last updated")

    class Meta:
        verbose_name = "StatusTV Admin"
        verbose_name_plural = "Status"


class StorageTV(models.Model):
    tvid = models.ForeignKey(DisplayTV, on_delete=models.CASCADE, null=True, blank=True, related_name="storage_tvs", verbose_name="Display")
    storage = models.CharField(max_length=100, verbose_name="Empty Storage")
    time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True, verbose_name="Last updated")


    class Meta:
        verbose_name = "StorageTV Admin"
        verbose_name_plural = "Storage"

class VolumeTV(models.Model):
    displaytv = models.OneToOneField(DisplayTV, on_delete=models.CASCADE, related_name="volumetv", verbose_name="Select TV")
    volume_tv = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self):
        return f"{self.displaytv} - {self.volume_tv}"
    

    class Meta:
        verbose_name = "Volume Admin"
        verbose_name_plural = "Volume"



class MediaSystem(models.Model):
    production_line = models.ForeignKey(ProductionLine,on_delete=models.CASCADE, null=True, blank=True, related_name="select_production_line")
    select_folder =  models.ForeignKey (MediaBucket,on_delete=models.CASCADE,related_name="folder_names")
    select_tv = models.ForeignKey(DisplayTV, on_delete=models.CASCADE, null=True, blank=True, related_name="select_tv", verbose_name="Display")
    duration = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)






class ProductionLineTV(models.Model):
    production_line = models.ForeignKey('ProductionLine', on_delete=models.CASCADE)
    display_tv = models.ForeignKey('DisplayTV', on_delete=models.CASCADE)
    status = models.CharField(max_length=100)



    def __str__(self):
        return f"{self.production_line}"



# sop/models.py



# used by developer only

class ClientUserMap(models.Model):
    username = models.CharField(max_length=150)
    db_name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('username', 'db_name')  # ✅ combo unique

    def __str__(self):
        return f"{self.username} -> {self.db_name}"




class MachineRuntime(models.Model):
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url





class Client(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=255)
    database_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)