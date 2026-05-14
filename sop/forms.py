from django import forms
from .models import Admin, ProductionAdmin, ProductionLine, DisplayTV, MediaContent, MediaFile, VolumeTV, MediaBucket
from django.contrib.auth.models import User
from .widgetss import FileWithSelectButtonWidget
from django.core.validators import MinValueValidator, MaxValueValidator


# FIX: ClearableFileInput ko multiple files support karne ke liye
class ClearableMultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class AdminnForm(forms.ModelForm):
    class Meta:
        model = Admin
        exclude = ['created_by', 'user']

    def clean_admin_username(self):
        username = self.cleaned_data.get("admin_username")
        user_id = self.instance.user_id

        model_class = self.instance._meta.model

        print("What is this", model_class._meta.verbose_name, type(model_class._meta.verbose_name))

        if model_class._meta.verbose_name == "Admin":

            if User.objects.filter(username=username).exclude(id=user_id).exists():
                raise forms.ValidationError("This username is already taken. Please choose another.")

            return username

        elif model_class._meta.verbose_name == "Production Admin":

            print(model_class._meta.verbose_name)

            if ProductionAdmin.objects.count() == DisplayTV.objects.count():
                raise forms.ValidationError("Number of production admins cannot be greater than display tvs.")

            else:

                if User.objects.filter(username=username).exclude(id=user_id).exists():
                    raise forms.ValidationError("This username is already taken. Please choose another.")

                return username



class MediaContentForm(forms.ModelForm):

    files = forms.FileField(
        widget=ClearableMultipleFileInput(attrs={'multiple': True}),
        required=False
    )

    selected_files_ids = forms.CharField(
        required=False,
        widget=forms.HiddenInput
    )

    sequence_order = forms.IntegerField(
        required=False,
        min_value=1,
        label="Sequence",
        widget=forms.NumberInput(attrs={
            'class': 'sequence_order_field',
            'style': 'display:none; width:80px;'
        })
    )

    custom_action = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = MediaContent
        fields = ("display_tv", "duration", "sequence_order", "custom_action", "selected_files_ids")

        widgets = {
            'duration': forms.NumberInput(attrs={'style': 'width: 60px;', 'min': 1}),
            "production_line": forms.HiddenInput(),
        }

    def clean_files(self):

        if not hasattr(self.files, "getlist"):
            return self.cleaned_data.get("files")

        files = self.files.getlist(self.add_prefix('files'))

        if not files:
            return self.cleaned_data.get("files")

        custom_action = self.cleaned_data.get("custom_action") or self.data.get(self.add_prefix("custom_action"))
        print("Custom action =", custom_action)

        if custom_action == "true" and len(files) > 2:
            raise forms.ValidationError(
                "You cannot upload more than 2 files when using Sequence Order."
            )

        MAX_SIZE_MB = 400
        MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

        for f in files:
            print(f.size, "This is the video size")
            if f.size > MAX_SIZE_BYTES:
                raise forms.ValidationError(
                    f"{f.name} is too large. Max allowed size is {MAX_SIZE_MB} MB."
                )

        return files


class MediaFileForm(forms.ModelForm):

    sequence = forms.CharField(
        max_length=50,
        label="Sequence",
        widget=forms.TextInput()
    )

    duration = forms.IntegerField(
        min_value=1,
        label="Duration",
        widget=forms.NumberInput()
    )

    volume = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        label="Volume",
        widget=forms.NumberInput(attrs={"min": 0, "max": 100})
    )

    selected_files_ids = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = MediaFile
        fields = ['file', 'selected_files_ids', 'sequence', 'duration', 'volume']
        labels = {
            "file": "File",
        }
        widgets = {
            'file': FileWithSelectButtonWidget(),
        }

    class Media:
        js = ("js/mediafile_select_modal.js",)


class VolumeTVAdminForm(forms.ModelForm):
    class Meta:
        model = VolumeTV
        fields = "__all__"
        widgets = {
            "volume_tv": forms.NumberInput(attrs={
                "type": "range",
                "min": 0,
                "max": 100,
                "step": 1,
                "class": "volume-slider",
            }),
        }

    class Media:
        css = {
            "all": ("css/volume_slider.css",)
        }
        js = ("js/volume_slider.js",)


from django.forms.widgets import HiddenInput, ClearableFileInput

class MediaBucketForm(forms.ModelForm):
    files = forms.CharField()


    class Meta:
        model = MediaBucket
        fields = ()  # 'file' is handled manually

    def save(self, commit=True):
        # Return unsaved instance to satisfy admin
        return super().save(commit=False)

    def save_m2m(self):
        # Required by Django admin
        pass





class ProductionLineForm(forms.ModelForm):
    display_tv = forms.ModelMultipleChoiceField(
        queryset=DisplayTV.objects.all(),
        widget=forms.SelectMultiple(attrs={'size': '10'}),
        label="Select TVs"
    )

    class Meta:
        model = ProductionLine
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Change labels to include ID
        self.fields['display_tv'].label_from_instance = lambda obj: f"{obj.display_number} ({obj.id})"
