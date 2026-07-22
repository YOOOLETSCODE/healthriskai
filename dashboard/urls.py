from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("ai-assistant/", views.ai_assistant, name="ai_assistant"),
]