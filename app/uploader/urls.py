from rest_framework.routers import DefaultRouter
from .views import FileViewSet, filterview, getdataview
from django.urls import path


router = DefaultRouter()
router.register(r'files', FileViewSet, basename='files')

urlpatterns = [
    path('getdata/<int:pk>/<int:nrows>', getdataview, name='getdataview'),
    path('getdata/<int:pk>/filter/sort/<int:nrows>', filterview, name='filterview'),
]

urlpatterns += router.urls