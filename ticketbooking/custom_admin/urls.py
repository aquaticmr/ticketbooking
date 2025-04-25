from django.urls import path
from .views import (
    AdminDashboardView,
    AdminShowListView,
    AdminShowCreateView,
    AdminShowUpdateView,
    AdminShowDeleteView,
    AdminBookingListView,
)

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('shows/', AdminShowListView.as_view(), name='admin_show_list'),
    path('shows/create/', AdminShowCreateView.as_view(), name='admin_show_create'),
    path('shows/<int:pk>/update/', AdminShowUpdateView.as_view(), name='admin_show_update'),
    path('shows/<int:pk>/delete/', AdminShowDeleteView.as_view(), name='admin_show_delete'),
    path('bookings/', AdminBookingListView.as_view(), name='admin_booking_list'),
]