from django.urls import path
from .views import Annotate 

urlpatterns = [
    path('annotate/', Annotate.as_view(), name='my_api_view'),
]
