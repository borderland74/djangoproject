from django.conf.urls import url,include
from django.contrib import admin
from axf import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    url(r'^home/slideshows/$',views.Slideshows.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)