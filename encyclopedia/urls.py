from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki",views.wiki,name="wiki"),
   
    
    path("wiki/add/",views.add,name="add"),
    path("wiki/random/",views.randoms,name="random"),
    path("wiki/search/",views.search,name="search"),
    path("wiki/edit/",views.edit,name="edit"),
    
    path("wiki/<str:name>",views.read,name="name"),
    
    
]
