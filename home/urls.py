from django.conf.urls import url
from . import views

#url patterns for the home page
urlpatterns=[
    url(r'^$', views.index, name='index'),   #base home url simply goes to the index method in home/views.py
    url(r'^about/$', views.abt, name='abt'),
    url(r'^graph/$', views.get_image, name="graph.get_image")
]
