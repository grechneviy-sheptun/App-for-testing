from django.urls import path
from views import TestCreateView


urlpatterns = [
    path("create-test/", TestCreateView.as_view(), name="create-test"),
]
