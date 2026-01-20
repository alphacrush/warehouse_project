from django.contrib import admin
from .models import Godown, Crop, Transaction

# --- 1. ADMIN PANEL BRANDING ---
admin.site.site_header = "Warehouse Management System"
admin.site.site_title = "Warehouse Admin Portal"
admin.site.index_title = "Welcome to the Control Center"

# --- 2. MODEL CONFIGURATION ---

@admin.register(Godown)
class GodownAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity')
    search_fields = ('name',)

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # Display the new fields in the admin list
    list_display = ('date', 'type', 'party_name', 'crop', 'bags', 'stack_no', 'gate_pass')
    list_filter = ('type', 'godown', 'crop')
    search_fields = ('party_name', 'stack_no', 'gate_pass', 'truck_number')
    date_hierarchy = 'date'