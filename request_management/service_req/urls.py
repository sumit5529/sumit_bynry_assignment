from django.urls import path
from .views import ServiceRequestCreateView, ServiceRequestListView, ServiceRequestDetailView, ServiceRequestUpdateView, ServiceRequestDeleteView

app_name = 'service_req'
urlpatterns = [
    path('create/', ServiceRequestCreateView.as_view(), name='service_request_create'),
    path('', ServiceRequestListView.as_view(), name='service_request_list'),
    path('<int:pk>/', ServiceRequestDetailView.as_view(), name='service_request_detail'),
    path('<int:pk>/update/', ServiceRequestUpdateView.as_view(), name='service_request_update'),
    path('<int:pk>/delete/', ServiceRequestDeleteView.as_view(), name='service_request_delete'),
]
