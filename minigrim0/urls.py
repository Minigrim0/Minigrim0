from django.conf.urls import handler400, handler403, handler404, handler500
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from knox import views as knox_views
from rest_framework import routers

from blog import api as api_views
from minigrim0 import views as views
from minigrim0 import api as auth_views

router = routers.DefaultRouter()
router.register(r'posts', api_views.PostViewSet)
router.register(r'tags', api_views.TagViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path(r'auth/login/', auth_views.LoginView.as_view(), name='knox_login'),
    path(r'auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(r'auth/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path("admin/", admin.site.urls),
    path("dev/", include(("devlog.urls", "devlog"), namespace="devlog")),
    path("cv/", views.cv, name="cv"),
    path("cv/pdf/", views.cv_pdf, name="cv_pdf"),
    path("blog/", include(("blog.urls", "blog"), namespace="blog")),
    path("", views.index, name="index"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots")
]

handler404 = lambda req, *args, **kwargs: views.error(req, 404)
handler500 = lambda req, *args, **kwargs: views.error(req, 500)
handler403 = lambda req, *args, **kwargs: views.error(req, 403)
handler400 = lambda req, *args, **kwargs: views.error(req, 400)
