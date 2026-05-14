
from django.contrib import admin
import shutil
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Max
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import *
from .forms import *
from django.utils.html import format_html
from django.contrib.admin.views.main import ChangeList
from core.settings import BASE_DIR
from django.urls import path
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Count
import os
from django.template.response import TemplateResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from urllib.parse import unquote
from django.db import transaction
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from .middleware import get_current_client
from django.db.models import Min
from django import forms

class MyAdminSite(admin.AdminSite):
    site_header = "My Admin"
    site_title = "Admin Portal"
    index_title = "Dashboard"

    def each_context(self, request):
        context = super().each_context(request)
        # Yaha apna dynamic text
        context['site_header'] = "🔥 Ye hai aapka dynamic text! 🔥"
        return context

# default admin site replace karo
admin_site = MyAdminSite(name='myadmin')
# For User Model

class CustomUserAdmin(DefaultUserAdmin):
    list_display = ('username', 'is_active', 'is_staff', 'is_superuser')



    def get_readonly_fields(self, request, obj=None):
        if obj and request.user.username.endswith("@autofoam"
        ):
            return self.readonly_fields + ('is_superuser',)
        return self.readonly_fields



    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # ✅ ONLY ADD THIS CONDITION
        if request.user.is_superuser:
            return qs

        # 🔁 baaki same as it is
        if not request.user.is_superuser:
            qs = qs.filter(is_superuser=False)

        return qs.filter(groups__name=f"owner_{request.user.id}")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # ❌ BLOCK these fields completely
        if 'is_superuser' in form.base_fields and request.user.is_superuser == False:
            form.base_fields['is_superuser'].disabled = True

        if 'is_staff' in form.base_fields and request.user.is_superuser == False:
            form.base_fields['is_staff'].disabled = True

        if 'groups' in form.base_fields and request.user.is_superuser == False:
            form.base_fields['groups'].disabled = True

        if 'user_permissions' in form.base_fields:
            form.base_fields['user_permissions'].disabled = True

        return form

    def save_model(self, request, obj, form, change):
        # 🔥 FORCE RULE (main security)
        obj.is_superuser = False
        obj.is_staff = False

        super().save_model(request, obj, form, change)

        # 👇 OWNER SET (IMPORTANT)
        group, _ = Group.objects.get_or_create(
            name=f"owner_{request.user.id}"
        )

        obj.groups.add(group)



admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)






@admin.register(MediaBucket)
class MediaBucketAdmin(admin.ModelAdmin):
    form = MediaBucketForm
    list_display = ()  # Show fields in list
    list_display_links = ()    # Make folder_name clickable
    actions = ['delete_selected']     
    exclude = ('created_by',)  # ✅ hides field completely

    change_form_template = "admin/sop/mediabucket/mediabucket_change_form.html"
    class Media:
        js = ('js/media_bucket_validation.js',)





    def save_model(self, request, obj, form, change):
        """
        Handle multiple file uploads here.
        Each uploaded file creates a new MediaBucket instance.
        """
        files = request.FILES.getlist('files')
        folder_name = form.cleaned_data.get('folder_name')



        # 🔥 1️⃣ DELETE FOLDER ONLY ONCE
        folder_path = os.path.join(
            settings.MEDIA_ROOT,
            "upload",
            folder_name
        )

        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        # 🔥 2️⃣ DELETE DB RECORDS ONLY ONCE
        MediaBucket.objects.filter(folder_name=folder_name).delete()

        # 🔥 3️⃣ NOW SAVE ALL FILES


        max_sequence = MediaBucket.objects.filter(
            folder_name=folder_name
        ).aggregate(Max("sequence"))["sequence__max"] or 0


        for f in files:
            MediaBucket.objects.create(
                file=f,
                folder_name=folder_name,
                sequence = max_sequence + 1,
                created_by=request.user   # ✅ THIS IS THE KEY


            )




    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('folder/<str:folder_name>/', self.admin_site.admin_view(self.folder_detail_view), name='mediafolder_detail'),
            path(
                'folder/<str:folder_name>/delete/',
                self.admin_site.admin_view(self.delete_folder_view),
                name='mediafolder_delete'
            ),       
        ]
        return custom_urls + urls
    





    def delete_folder_view(self, request, folder_name):
            return format_html(
                f'<button type="button" class="button" onclick="publish(this)">Publish</button>',
            
            )
    def response_add(self, request, obj, post_url_continue=None):
        """
        Redirect after add + show Django success message.
        """

        # ✅ ADD MESSAGE (stored in session)
        messages.success(
            request,
            "Media bucket created successfully."
        )

        redirect_url = reverse("admin:sop_mediabucket_changelist")

        # AJAX request (your upload case)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "redirect_url": redirect_url
            })

        return super().response_add(request, obj, post_url_continue)

    

    # In MediaBucketAdmin
    def delete_folder_view(self, request, folder_name):
        folder_name = unquote(folder_name)
        folder_path = os.path.join(settings.MEDIA_ROOT, "upload", folder_name)

        # Delete folder from filesystem
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        # Delete all MediaBucket DB records
        MediaBucket.objects.filter(folder_name=folder_name).delete()

        # Success message
        messages.success(request, f"Folder '{folder_name}' deleted successfully.")

        # Redirect back to changelist
        return redirect("admin:sop_mediabucket_changelist")    


    def folder_detail_view(self, request, folder_name):
        folder_name = unquote(folder_name)

        # ✅ Folder ke saare files
        files = MediaBucket.objects.filter(
            folder_name=folder_name
        ).order_by('sequence')

        # ✅ Ek hi MediaSystem (folder ke liye)
        media_system = MediaSystem.objects.filter(
            select_folder__folder_name=folder_name
        ).first()

        # values
        media_system_id = media_system.id if media_system else None
        production_id = media_system.production_line_id if media_system else None
        duration = media_system.duration if media_system else 0

        data = MediaContent.objects.filter(production_line=production_id)
        # ✅ Sab files me SAME value
        for f in files:
            f.duration = duration
            f.is_published = False
            f.file_name = f.file.name.split("/")[-1]
            for  i in data:
                if i.filename == f.file.name:
                    f.duration = i.duration
                    f.is_published=i.is_published

            f.media_system_id = media_system_id
            f.production_id = production_id


        context = dict(
            self.admin_site.each_context(request),
            folder_name=folder_name,
            files=files,
            opts=self.model._meta,
        )

        return TemplateResponse(
            request,
            "admin/sop/mediabucket/mediafolderdetail.html",
            context,
        )



    # Inject distinct folder names into `cl.folders`
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            # Get distinct folder names
            folders = MediaBucket.objects \
                .exclude(folder_name__isnull=True) \
                .exclude(folder_name__exact='') \
                .values_list('folder_name', flat=True) \
                .distinct()
            # Attach folders to `cl` so template can access them
            response.context_data['cl'].folders = folders
        except (AttributeError, KeyError):
            pass
        return response





# For Admin Model

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    form = AdminnForm
    list_display = ('admin_username', 'created_by')


    def save_model(self, request, obj, form, change):
        # Set created_by automatically
        if not obj.created_by:
            obj.created_by = request.user

        # Handle linked User creation or update
        if not obj.user_id:
            # Create the User if it doesn't exist
            user = User.objects.create_user(
                username=obj.admin_username,
                password=obj.admin_password,
                is_staff=True,
                is_superuser=False
            )
            group = Group.objects.get(name='AdminRight')
            user.groups.add(group)
            obj.user = user
        else:
            # Update existing User
            user = obj.user
            if obj.admin_username:
                user.username = obj.admin_username
            if obj.admin_password:
                user.set_password(obj.admin_password)
            user.save()

        super().save_model(request, obj, form, change)



# # For Display model

@admin.register(DisplayTV)
class DisplayAdmin(admin.ModelAdmin):
    list_display = ["display_number",]





# For ProductionAdmin Model

@admin.register(ProductionAdmin)
class ProductionAdminAdmin(admin.ModelAdmin):
    form = AdminnForm
    list_display = ('admin_username', 'created_by')


    def save_model(self, request, obj, form, change):

        # Set created_by automatically
        if not obj.created_by:
            obj.created_by = request.user

        # Handle linked User creation or update
        if not obj.user_id:
            # Create the User if it doesn't exist
            user = User.objects.create_user(
                username=obj.admin_username,
                password=obj.admin_password,
                is_staff=True,
                is_superuser=False
            )

            obj.user = user
        else:
            # Update existing User
            user = obj.user
            if obj.admin_username:
                user.username = obj.admin_username
            if obj.admin_password:
                user.set_password(obj.admin_password)
            user.save()

        super().save_model(request, obj, form, change)




# #### After for multiple media files



class MediaContentInline(admin.TabularInline):
    model = MediaContent
    form = MediaContentForm
    extra = 1
    fields = ("display_tv", "duration", "files", "selected_files_ids","select_file_button", "filename_button","select_files_button")
    can_delete = False
    readonly_fields = ("select_file_button","select_files_button","filename_button")
    



    def select_files_button(self, obj):
        """
        Renders a button for both:
        - existing inline rows
        - newly added inline rows
        """
        return format_html(
            '<button type="button" class="button select-files-btn">'
            'Select Files</button>'
        )

    select_files_button.short_description = "Media Bucket"


    def select_file_button(self, obj):
        """
        Safe Upload button:
        - Works for new unsaved inline rows
        - Uses 0 as default if obj has no related TV or ProductionLine
        """
        tv_id = obj.display_tv.id if hasattr(obj, "display_tv") and obj.display_tv else 0
        production_id = obj.production_line.id if hasattr(obj, "production_line") and obj.production_line else 0

        return format_html(
            '<button type="button" onclick="uploadImage(this);" id="{}+{}" class="button upload-files-btn">'
            'Upload</button>',
            tv_id,
            production_id
        )

    select_file_button.short_description = "Upload"




    def filename_button(self, obj):
        if not obj.display_tv:
            return "-"

        from .models import MediaContent

        # 🔥 same TV ka latest / first MediaContent
        media = MediaContent.objects.filter(display_tv=obj.display_tv).first()

        filename = media.filename if media and media.filename else "-"

        return format_html(
            '<span>{}</span>',
            filename
        )

    filename_button.short_description = "Filename"













    # def select_file_button_bucket(self, obj):
    #     """
    #     Safe Upload button:
    #     - Works for new unsaved inline rows
    #     - Uses 0 as default if obj has no related TV or ProductionLine
    #     """
    #     tv_id = obj.display_tv.id if hasattr(obj, "display_tv") and obj.display_tv else 0
    #     production_id = obj.production_line.id if hasattr(obj, "production_line") and obj.production_line else 0

    #     return format_html(
    #         '<button type="button" onclick="uploadImage(this);" id="{}+{}" class="button upload-bucket-files-btn">'
    #         '⬆️</button>',
    #         tv_id,
    #         production_id
    #     )

    # select_file_button_bucket.short_description = "Bucket"








    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "display_tv":
            # Get the ProductionLine ID from admin URL
            productionline_id = request.resolver_match.kwargs.get("object_id")

            if productionline_id:
                from .models import ProductionLine
                try:
                    pl = ProductionLine.objects.get(id=productionline_id)
                except ProductionLine.DoesNotExist:
                    pass

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    



@admin.register(ProductionLine)
class ProductionLineAdmin(admin.ModelAdmin):
    list_display = ("productionline_name", "description", "associated_tvs", "created_by", "active_line",)
    exclude = ("created_by", "created_at", "updated_at")
    inlines = [MediaContentInline]
    form = ProductionLineForm


    change_form_template = "admin/sop/productionline/change_form.html"

    class Media:
        js = ("js/media_content_inline.js",)
        css = {
            "all": ("css/media_bucket_modal.css",)
        }

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'mediabucket/select/',
                self.admin_site.admin_view(self.media_bucket_select),
                name='media_bucket_select'
            ),
            path(
                'mediabucket/files/',
                self.admin_site.admin_view(self.media_bucket_files),
                name='media_bucket_files'
            ),
        ]
        return custom_urls + urls
    



    # -----------------------------
    # AJAX-aware redirect after save
    # -----------------------------
    def response_change(self, request, obj):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            # Add a success message (optional: also store in session if needed)
            msg = "Your details have been saved successfully !!"
            messages.success(request, msg)
            return JsonResponse({
                "redirect_url": reverse("admin:sop_mediacontent_changelist"),
                "message": msg
            })
        return super().response_change(request, obj)


    def response_add(self, request, obj, post_url_continue=None):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            msg = "Your details have been saved successfully !!"
            messages.success(request, msg)
            return JsonResponse({
                "redirect_url": reverse("admin:sop_productionline_changelist"),
                "message": msg
            })
        return super().response_add(request, obj, post_url_continue)
    
    @xframe_options_exempt
    def media_bucket_select(self, request):
        folders = MediaBucket.objects.values('folder_name').annotate(file_count=Count('id')).order_by('folder_name')
        context = {'folders': folders}
        return TemplateResponse(request, "admin/sop/mediabucket/modal_folders.html", context)
    

    @xframe_options_exempt
    def media_bucket_files(self, request):
        folder_name = request.GET.get("folder_name")
        files = MediaBucket.objects.filter(folder_name=folder_name)
        context = {'files': files}
        return TemplateResponse(request, "admin/sop/mediabucket/modal_files.html", context)



    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == "POST":
            request.POST = request.POST.copy()

            # 🔥 force save button
            if '_save' not in request.POST:
                request.POST['_save'] = 'Save'

        return super().change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.save()

        # 🔥 TV order capture  


    def save_formset(self, request, form, formset, change):

        # First let Django save the inline normally
        instances = formset.save(commit=False)
        

        for form in formset.forms:
            

            file_array = []

            selected_files_id = [
                int(i)
                for i in form.data.get(f"{form.prefix}-selected_files_ids", "").split(",")
                if i
            ]

            for fileid in selected_files_id:
                print(fileid, type(fileid))
                print(MediaBucket.objects.get(id=fileid).folder_name, MediaBucket.objects.get(id=fileid).file)
                file_array.append(MediaBucket.objects.get(id=fileid).file)

            print(file_array)
            
            if not form.cleaned_data:
                continue

            # Skip deleted forms
            if form.cleaned_data.get('DELETE', False):
                if form.instance.pk:
                    form.instance.delete()
                continue

            media_instance = form.save(commit=False)
            media_instance.production_line = formset.instance
            media_instance.save()

            sequence_order = form.cleaned_data.get("sequence_order")
            # print("Sequence Order Received:", sequence_order)
            

            # Use file_array if available, else fallback to uploaded files
            files_to_process = file_array or request.FILES.getlist(f"{form.prefix}-files")

            if sequence_order == None:
                # Correct way to get uploaded files
                uploaded_files = request.FILES.getlist(f"{form.prefix}-files")
                # print("uploaded_files", uploaded_files)

                for f in files_to_process:

                    # 🔥 HAR FILE KE LIYE NAYA MediaContent (duplicate allowed)
                    media_content_obj = MediaContent.objects.create(
                        production_line=media_instance.production_line,
                        display_tv=media_instance.display_tv,
                        duration=media_instance.duration
                    )

                    # 🔥 HAR FILE KE LIYE MediaFile
                    MediaFile.objects.create(
                        media_content=media_content_obj,
                        file=f,
                        order="auto"
                    )
            elif sequence_order != None:


                for f in files_to_process:
                    media_content_obj, created = MediaContent.objects.update_or_create(
                        production_line=media_instance.production_line,
                        display_tv=media_instance.display_tv,
                        duration=media_instance.duration,
                        defaults={
                            "production_line": media_instance.production_line,
                            "display_tv": media_instance.display_tv,
                            "duration": media_instance.duration
                        }
                    )

                    MediaFile.objects.update_or_create(
                        media_content=media_content_obj,
                        file=f,
                        order=sequence_order,
                        defaults={
                            "media_content": media_content_obj,
                            "file": f,
                            "order": sequence_order
                        }
                    )



class MediaContentRow:
    def __init__(self, base, file_obj):
        self._base = base
        self.single_file = file_obj

    def __getattr__(self, item):
        return getattr(self._base, item)
    



class MediaContentChangeList(ChangeList):

    def get_results(self, request):

        super().get_results(request)

        expanded = []

        for obj in self.result_list:
            files = obj.files.all()
            if files.exists():
                for file_obj in files:
                    # print(file_obj, "What is inside this ?", type(file_obj))
                    expanded.append(MediaContentRow(obj, file_obj))
            else:
                expanded.append(MediaContentRow(obj, None))

        self.result_list = expanded
        self.full_result_count = len(expanded)
        self.result_count = len(expanded)



class MediaContentAdmin(admin.ModelAdmin):
    list_display = ('display_tv','edit_tv_name', 'production_line', 'duration', 'tv_volume',  'single_file_display', 'single_file_order', 'row_actions',)
    list_select_related = ('display_tv', 'production_line')
    list_display_links = None
    list_filter = ('display_tv','production_line')
    





    class Media:
        js = ('js/media_toggle.js','js/test.js')


        
    # def select_mediafile_checkbox(self,obj):
    #     if obj.single_file:
            
    #         return format_html(
    #             '<input type="checkbox" class="mediafile-checkbox" value="{}"><button id="handlebtn" class="btn btn-danger" onclick="javascript:deletetest();" style="top:-100px;right:0px;position:absolute;">Delete</button>', obj.single_file.id,
    #         )
    # select_mediafile_checkbox.short_description = "Select"

    # def get_actions(self, request):
    #     # Disable default "delete selected" checkbox
    #     actions = super().get_actions(request)    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions




    def get_fields(self, request, obj=None):

        # start with default model fields
        fields = list(super().get_fields(request, obj))
    
        # insert virtual field just after display_tv
        if "display_tv" in fields and "display_number" not in fields:
            index = fields.index("display_tv") + 1
            fields.insert(index, "display_number")
    
        return fields


    def get_changelist(self, request, **kwargs):
        
        return MediaContentChangeList

    def single_file_display(self, obj):

        if obj.single_file:
            f = obj.single_file

            # final = BASE_DIR + f.file.url

            # print(final)
            return format_html('<a href="{}" target="_blank">{}</a>', f.file.url, f.file.name)
        return "-"
    single_file_display.short_description = "Media File"


    
    

    def single_file_order(self, obj):

        if obj.single_file:
            f = obj.single_file

            return f.order
        return "-"
    single_file_order.short_description = "Sequence"
    
    
    def tv_volume(self, obj):
        if obj.display_tv:
            tv = obj.display_tv

            # final = BASE_DIR + f.file.url

            # print(final)
            return tv.volumetv.volume_tv
        return "-"
    tv_volume.short_description = "Volume"
    


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "edit-tv/<int:tv_id>/",
                self.admin_site.admin_view(self.edit_tv_view),
                name="mediacontent-edit-tv",
            ),
            path(
                'file/<int:file_id>/<int:mediacontent_id>/custom_update/',
                self.admin_site.admin_view(self.custom_file_update_view),
                name='mediacontent-file-update'
            ),
            path(
                'file/<int:file_id>/custom_delete/',
                self.admin_site.admin_view(self.custom_file_delete_view),
                name='mediacontent-file-delete'
            ),
            
        ]
        return custom_urls + urls

    

    def row_actions(self, obj):
        
        # Check if a MediaFile exists
        if obj.single_file:
            f = obj.single_file
            update_url = reverse('admin:mediacontent-file-update', args=[f.id, obj.id])
            delete_url = reverse('admin:mediacontent-file-delete', args=[f.id])
            delete_row = reverse('admin:mediacontent-file-delete', args=[f.id])
            return format_html(
                '<a href="{}">Update</a>&nbsp;&nbsp;&nbsp;<a href="{}"><i class="fa fa-trash"></i></a>',
                update_url,delete_row
            )
        # If no file exists, either return "-" or disabled buttons
        return format_html(
            '<span style="color:gray;">Update</span>&nbsp;<span style="color:gray;">Delete</span>'
        )
    



    def custom_file_update_view(self, request, file_id, mediacontent_id):
        f = get_object_or_404(MediaFile, id=file_id)
        # media_content_obj = f.media_content

        media_content_object = get_object_or_404(MediaContent, id=mediacontent_id)


        # Get or create VolumeTV for this DisplayTV
        volume_obj, _ = VolumeTV.objects.get_or_create(
            displaytv=media_content_object.display_tv
        )

        print(mediacontent_id, "What is inside it ?")


        if request.method == "POST":
                form = MediaFileForm(request.POST, request.FILES, instance=f)
                print(form.is_valid())
                if form.is_valid():
                    with transaction.atomic():

                        obj = form.save(commit=False)

                        # -----------------------------
                        # 1️⃣ Handle file selection logic (UNCHANGED)
                        # -----------------------------
                        selected_files_ids = form.cleaned_data.get("selected_files_ids", "")

                        print(selected_files_ids)
                        if selected_files_ids:
                            obj.file = MediaBucket.objects.get(id=selected_files_ids).file
                        else:
                            if "file" in request.FILES:
                                obj.file = request.FILES["file"]

                        obj.media_content = media_content_object

                        # -----------------------------
                        # 2️⃣ Update MediaFile (sequence → order)
                        # -----------------------------
                        obj.order = form.cleaned_data["sequence"]
                        obj.save()

                        # -----------------------------
                        # 3️⃣ Update MediaContent (duration)
                        # -----------------------------
                        media_content_object.duration = form.cleaned_data["duration"]
                        media_content_object.save()

                        # -----------------------------
                        # 4️⃣ Update VolumeTV (volume)
                        # -----------------------------
                        volume_obj.volume_tv = form.cleaned_data["volume"]
                        volume_obj.save()
                        
                        # 5️⃣ Update DisplayTV.display_number
                        display_number = form.cleaned_data.get("display_number")
                        if display_number:
                            media_content_object.display_tv.display_number = display_number
                            media_content_object.display_tv.save(update_fields=["display_number"])

                    messages.success(
                        request,
                        f"Your detail have been updated successfully!"
                    )
                    # return redirect("admin:sop_mediacontent_changelist")

                    # ✅ ADDED: AJAX RESPONSE FOR BACKDROP / PROGRESS BAR
                    if request.headers.get("x-requested-with") == "XMLHttpRequest":
                        return JsonResponse({
                            "success": True,
                            "redirect_url": reverse("admin:sop_mediacontent_changelist")
                        })

                    # ✅ EXISTING REDIRECT (UNCHANGED)
                    return redirect("admin:sop_mediacontent_changelist")

        else:
            # -----------------------------
            # Pre-fill form values
            # -----------------------------
            form = MediaFileForm(
                instance=f,
                initial={
                    "sequence": f.order,
                    "duration": media_content_object.duration,
                    "volume": volume_obj.volume_tv,
                }
            )


        context = self.admin_site.each_context(request)
        context.update({
            "form": form,
            "media_file": f,
            "media_content": media_content_object,
        })
        return render(request, "admin/sop/mediacontent/custom_file_update.html", context)




    def custom_file_delete_view(self, request, file_id):
        # 🔹 Debugging
        print("Deleting MediaFile", file_id)

        f = get_object_or_404(MediaFile, id=file_id)
        media_content = f.media_content  # Parent MediaContent

        # Delete the MediaFile
        f.delete()

        # Check if MediaContent has any files left
        if not media_content.files.exists():
            media_content.delete()
            messages.success(request, f"All files deleted. MediaContent also removed!")
        else:
            messages.success(request, f"{f.file.name} deleted successfully!")

        return redirect('admin:sop_mediacontent_changelist')

        
        
    def has_add_permission(self, request):
        return False   # disables “Add MediaContent” button
        
    def edit_tv_name(self, obj):

        if obj.display_tv:
            url = reverse(
                "admin:mediacontent-edit-tv",
                args=[obj.display_tv.id]
            )
            return format_html(
                '<a href="{}" title="Edit TV Name" style="font-size:18px;">✏️</a>',
                url
            )

        return "-"
        
    def edit_tv_view(self, request, tv_id):
        tv = get_object_or_404(DisplayTV, id=tv_id)
    
        if request.method == "POST":
            new_name = request.POST.get("display_number")
            if new_name:
                tv.display_number = new_name
                tv.save(update_fields=["display_number"])
                messages.success(request, "TV name updated successfully.")
                return redirect("admin:sop_mediacontent_changelist")
    
        context = dict(
            self.admin_site.each_context(request),
            tv=tv,
        )
    
        return render(request, "admin/sop/mediacontent/edit_tv_name.html", context)
    
    
        edit_tv_name.short_description = " " 



admin.site.register(MediaContent, MediaContentAdmin)












@admin.register(VolumeTV)
class VolumeTvAdmin(admin.ModelAdmin):
    form = VolumeTVAdminForm
    list_display = ('displaytv', 'volume_tv')
    search_fields = (
        'displaytv__display_number',  # 🔥 search by TV1 / TV2
    )

    readonly_fields = ('displaytv_label',)

    def get_fields(self, request, obj=None):
        if obj:  # CHANGE view
            return ('displaytv_label', 'volume_tv')
        # return ('displaytv', 'volume_tv')  # ADD view

    def displaytv_label(self, obj):
        return obj.displaytv.display_number  # or str(obj.displaytv)

    displaytv_label.short_description = "TV Number"






@admin.register(StorageTV)
class StorageTvAdmin(admin.ModelAdmin):
    list_display = ('tvid', 'storage', 'updated_time')
    list_display_links = None

    search_fields = (
        'tvid__display_number',  # 🔥 search by TV1 / TV2
    )

@admin.register(StatusTV)
class StatusTvAdmin(admin.ModelAdmin):
    list_display = ('tvid', 'updated_time', 'statustv')
    list_display_links = None
    change_list_template = "admin/sop/statustv/change_list.html"  # ✅ ADD THIS
    search_fields = ('tvid__display_number',)


    def statustv(self, obj):
        if obj.status:
            return format_html(f'<span style="color:green;">{obj.status}</span>') if obj.status == "ONLINE" else format_html(f'<span style="color:red;">{obj.status}</span>')
        return "-"
    

    statustv.short_description = "Status"
    statustv.admin_order_field = "status"






class MediaSystemForm(forms.ModelForm):
    
    class Meta:
        model = MediaSystem
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        production_line_id = self.data.get("select_tv")
        bucket_id = self.data.get("select_folder")

        if production_line_id and bucket_id:
            try:
                bucket = MediaBucket.objects.get(id=bucket_id)

                # file name without extension
                file_name = os.path.splitext(
                    os.path.basename(bucket.file.name)
                )[0]

                # production line ke TVs filter karo
                self.fields["select_tv"].queryset = DisplayTV.objects.filter(
                    production_line_id=production_line_id,
                    name=file_name
                )

            except MediaBucket.DoesNotExist:
                pass





class MediaSystemAdmin(admin.ModelAdmin):
    list_display = ('select_folder','production_line', 'duration','Upload')
    exclude = ('is_published',)


    class Media:
        js = ('js/test.js',)


    def Upload(self, obj):
        
        if not obj.is_published:

            return format_html(
                f'<button type="button" class="button" id="{obj.production_line.id}+{obj.select_folder.id}+{obj.duration}+{obj.id}" onclick="publish(this)">Publish</button>',
            
            )        
        else:

            return format_html(
                f'<button type="button" onclick="deletedata(this)" class="button" id="{obj.production_line.id}+{obj.select_folder.id}+{obj.duration}+{obj.id}">Unpublished</button>',
            
            )


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'get-images/',
                self.admin_site.admin_view(self.get_tvs),
                name='get_images',
            ),
        ]
        return custom_urls + urls

    def get_tvs(self, request):

        bucket_name = request.GET.get('bucket_name')
        production_id = request.GET.get("production_line_id")
        #tvs = DisplayTV.objects.filter(production_line_id=bucket_id)
        media_images = MediaBucket.objects.filter(folder_name=bucket_name).order_by('sequence')
        
        production = ProductionLine.objects.get(id=production_id)

        tvs = production.display_tv.all()
        result = []


        if len(media_images) >= len(tvs):
            for i in media_images:
                image_name = str(i.file).split("/")[-1]
                for u in tvs:
                    if u.display_number in image_name:
                        result.append({"id":u.id,"name":u.display_number,"image":image_name}) 

        return JsonResponse(result, safe=False)



    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "select_folder":
            subquery = (
                MediaBucket.objects
                .values('folder_name')
                .annotate(min_id=Min('id'))
                .values_list('min_id', flat=True)
            )
            kwargs["queryset"] = MediaBucket.objects.filter(id__in=subquery)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    




@admin.register(ProductionLineTV)
class ProductionLineTVAdmin(admin.ModelAdmin):
    list_display = ('production_line', 'display_tv', 'status')


    readonly_fields = ("production_line", "display_tv", "status")
    def get_list_display_links(self, request, list_display):
            return None

    # Add/Edit/Delete disable
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False




ALLOWED_DBS = ['micromatic']

class MachineRuntimeAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return get_current_client() in  ALLOWED_DBS

    def has_view_permission(self, request, obj=None):
        return get_current_client() in ALLOWED_DBS
admin.site.register(MachineRuntime, MachineRuntimeAdmin)








SUPERDB = ["default"]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return (
            get_current_client() in SUPERDB and
            request.user.is_superuser
        )

    def has_view_permission(self, request, obj=None):
        return (
            get_current_client() in SUPERDB and
            request.user.is_superuser
        )

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser





admin.site.register(MediaSystem,MediaSystemAdmin)
