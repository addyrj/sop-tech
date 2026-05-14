# widgets.py
from django.forms.widgets import Widget
from django.utils.safestring import mark_safe

class FileWithSelectButtonWidget(Widget):
    template_name = None  # Render HTML manually

    def render(self, name, value, attrs=None, renderer=None):
        file_input = f'<input type="file" name="{name}" id="id_{name}">'
        button = '<button type="button" class="button select-files-btn">Select File</button>'
        return mark_safe(f'<div style="display:flex; gap:10px; align-items:center;">{file_input}{button}</div>')