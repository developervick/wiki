from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entryPage, name="entryPage"),
    path("search/", views.search, name="search"),
    path("createPage/", views.createPage, name="createPage"),
    path('random/', views.RandomPage, name="randomPage"),
    path('editPage/', views.editPage, name="editPage"),
    path('updateEntry/', views.updateEntry, name="updateEntry")
]


