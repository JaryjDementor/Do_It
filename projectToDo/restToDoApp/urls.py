from django.urls import path
from .views import WorkersTasksAPIView

urlpatterns = [
    path("api/v1/workerslist/", WorkersTasksAPIView.as_view()),
]
