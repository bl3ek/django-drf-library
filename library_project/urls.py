from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Підключаємо наші апі-ендпоінти з префіксом api/
    path('api/', include('library.urls', namespace='library')),
]

# Налаштування для відображення медіа-файлів у режимі розробки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)