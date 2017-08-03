from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('pompom.apps.huddle_board.urls', namespace="pompom"))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
