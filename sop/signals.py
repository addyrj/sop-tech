from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from django.db.models.signals import m2m_changed
from .models import MediaFile,MediaBucket
import os,shutil
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import get_user_model
from sop.models import ClientUserMap
from sop.middleware import get_current_client
from django.core.management import call_command


_deleted_folders = set()   # 🔥 global tracker

@receiver(post_delete, sender=Admin)
def delete_admin_reference_from_user(sender, instance, **kwargs):
    User.objects.get(id=instance.user_id).delete()
    print("Reference deleted")

@receiver(post_delete, sender=ProductionAdmin)
def delete_productionadmin_reference_from_user(sender, instance, **kwargs):
    User.objects.get(id=instance.user_id).delete()
    print("Reference deleted")
    
    


@receiver(post_save, sender=DisplayTV)
def create_user_for_displaytv_and_setvolumetv(sender, instance, created, **kwargs):
    if created and instance.user is None:
        username = f"display_{instance.display_number}"

        user = User.objects.create_user(
            username=username,
            password=User.objects.make_random_password()
        )

        instance.user = user
        instance.save(update_fields=["user"])

        VolumeTV.objects.create(displaytv=instance, volume_tv=0)

        print("Signal run : User instance for displaytv and VolumeTV have been created!")






@receiver(m2m_changed, sender=ProductionLine.display_tv.through)
def create_production_line_tv(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for tv_id in pk_set:
            ProductionLineTV.objects.get_or_create(
                production_line=instance,
                display_tv_id=tv_id,
                defaults={"status": "pending"}
            )




User = get_user_model()

@receiver(post_save, sender=User)
def store_user_mapping(sender, instance, created, **kwargs):
    if not created:
        return

    username = instance.username

    # 🔥 current DB detect karo
    current_db = get_current_client() or "default"

    # 🔥 mapping save karo master DB me
    ClientUserMap.objects.using('user_credential_master').get_or_create(
        username=username,
        defaults={"db_name": current_db}
    )

    print(f"Mapping saved: {username} -> {current_db}")


 






@receiver(post_save, sender=Client)

def setup_client(sender, instance, created, **kwargs):

    if not created:
        return


    db = instance.database_name

    print("🚀 Setting up:", db)

    # 🔥 1. migrate DB
    call_command('migrate', database=db, interactive=False)

    # 🔥 2. create user in that DB
    user = User(
        username=instance.username,
        email=instance.email or "",
        is_staff=True,
        is_superuser=True
    )

    # 🔥 password set (IMPORTANT)
    user.set_password(instance.password)
    # 🔥 save in correct DB
    user.save(using=db)

    print("✅ Superuser created in:", db)




@receiver(post_delete, sender=Client)
def delete_client_user(sender, instance, **kwargs):

    db = instance.database_name

    print("🗑️ Deleting users in DB:", db)

    # 🔥 delete all users from that DB (or specific one)
    User.objects.using(db).filter(username=instance.username).delete()

    print("✅ User deleted from:", db)
    