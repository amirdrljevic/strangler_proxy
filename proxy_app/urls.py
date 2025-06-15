from django.urls import re_path
from . import views

urlpatterns = [
    # ^.*$ matches any path
    re_path(r"^.*$", views.proxy_home, name="proxy_home"),
]
