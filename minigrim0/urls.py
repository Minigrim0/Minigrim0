from django.conf.urls import handler400, handler403, handler404, handler500
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

import minigrim0.views as views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dev/", include(("devlog.urls", "devlog"), namespace="devlog")),
    path("cv/", views.cv, name="cv"),
    path("blog/", include(("blog.urls", "blog"), namespace="blog")),
    path("", views.index, name="index"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots")
]

handler404 = lambda req, *args, **kwargs: views.error(req, 404)
handler500 = lambda req, *args, **kwargs: views.error(req, 500)
handler403 = lambda req, *args, **kwargs: views.error(req, 403)
handler400 = lambda req, *args, **kwargs: views.error(req, 400)
