from django.urls import path
from .views import MachineAPIView,OEECalculationAPIView
urlpatterns=[
    path('machines',MachineAPIView.as_view(),name='machine'),
    path('machine-oee',OEECalculationAPIView.as_view(),name='oee_calculation'),
]