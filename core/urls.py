from django.contrib import admin
from django.urls import path
from inventory import views  # <--- IMPORT FROM INVENTORY APP

urlpatterns = [
    # 1. Admin
    path('admin/', admin.site.urls),

    # 2. Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # 3. Transactions
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('print/<int:transaction_id>/', views.print_receipt, name='print_receipt'),
    
    # 4. Reports & Data
    path('reports/', views.reports, name='reports'),
    path('import/', views.import_data, name='import_data'),
    path('party/<str:party_name>/', views.party_detail, name='party_detail'),
    path('godown/<int:godown_id>/', views.godown_detail, name='godown_detail'),
    
    # 5. Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # In core/urls.py, add this line inside urlpatterns:
    path('registers/', views.registers_view, name='registers_view'),
]