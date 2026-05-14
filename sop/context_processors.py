import os
from .models import DisplayTV, MediaBucket

def dashboard_text(request):
    if request.path.startswith('/admin') and request.user.is_authenticated:

        tv_count = DisplayTV.objects.count()
        media_files = MediaBucket.objects.filter(created_by=request.user)

        total_size = 0

        for media in media_files:
            if media.file:
                file_path = media.file.path
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)

        # 🔥 Smart size conversion
        if total_size < 1024:
            size_str = f"{total_size} Bytes"
        elif total_size < 1024**2:
            size_str = f"{total_size / 1024:.2f} KB"
        elif total_size < 1024**3:
            size_str = f"{total_size / (1024**2):.2f} MB"
        else:
            size_str = f"{total_size / (1024**3):.2f} GB"

        msg = f"{size_str} / {tv_count} GB"

        return {
            'dynamic_dashboard_text': msg,
            'storage_used': size_str,
            'tv_count': tv_count,
        }

    return {}