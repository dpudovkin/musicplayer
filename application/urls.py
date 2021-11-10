from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from application.views import index
from chat.views import chat

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rooms/', include("room.urls")),
    path('', index),
    path('chat/', chat)

]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
