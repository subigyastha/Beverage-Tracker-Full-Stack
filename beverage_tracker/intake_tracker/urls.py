from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # List and Home
    path('', views.BeverageEntryListView.as_view(), name='beverage_entry_list'),
    
    # Detail View
    path('entry/<int:pk>/', views.BeverageEntryDetailView.as_view(), name='beverage_entry_detail'),
    
    # Create New Entry
    path('new/', views.create_beverage_entry, name='beverage_entry_create'),
    
    # Update Existing Entry
    path('edit/<int:pk>/', views.edit_beverage_entry, name='beverage_entry_update'),
    
    # Delete Entry
    path('delete/<int:pk>/', views.BeverageEntryDeleteView.as_view(), name='beverage_entry_delete'),
    
    # Advanced Filtering
    path('filter/', views.beverage_entry_filter, name='beverage_entry_filter'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


