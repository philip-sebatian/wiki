from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki",views.wiki,name="wiki"),
   
    path("wiki/<str:name>",views.read,name="name"),
    path("add",views.add,name="add"),
    path("random",views.randoms,name="random")
]
