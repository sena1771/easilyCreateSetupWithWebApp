from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('',views.home,name = 'home'),
    path('run-python-script/',views.run_python_script,name='run_python_script'),
    path('download-zip/',views.download_zip,name='download_zip'),
    #path('upload/',views.uploaded_file,name='upload_file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)