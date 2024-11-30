from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500, handler403, handler400

import minigrim0.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dev/', include(("devlog.urls", "devlog"), namespace="devlog")),
    path('cv/', views.cv, name="cv"),
    path("blog/", include(("blog.urls", "blog"), namespace="blog")),
    path('', views.index, name="index"),
]

handler404 = lambda req, *args, **kwargs: views.error(req, 404)
handler500 = lambda req, *args, **kwargs: views.error(req, 500)
handler403 = lambda req, *args, **kwargs: views.error(req, 403)
handler400 = lambda req, *args, **kwargs: views.error(req, 400)
