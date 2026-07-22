from django.urls import path
from . import views

app_name = "patients"

urlpatterns = [
    path("new/",views.new_assessment,name="new_assessment"),
    path('history/',views.history,name="history"),
    path("history/<int:id>/", views.history_detail, name="history_detail"),
    path("delete/<int:id>/", views.delete_assessment, name="delete_assessment")
]