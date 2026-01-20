from django.db import models
from django.utils import timezone

# --- 1. MASTER DATA ---

class Godown(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    capacity = models.IntegerField(default=10000, help_text="Total Bags Capacity")

    def __str__(self): return self.name

class Crop(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=[('Rabi', 'Rabi'), ('Kharif', 'Kharif')], default='Rabi')

    def __str__(self): return self.name

# Note: StockBalance model is removed to prevent conflicts. 
# We now calculate stock directly from Transactions.

# --- 2. TRANSACTION MODEL (Merged & Updated) ---

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('SR', 'Stock Receipt (Deposit)'),
        ('DL', 'Delivery (Outgoing)'),
    )

    date = models.DateField(default=timezone.now)
    party_name = models.CharField(max_length=100, default="General", verbose_name="Person/Party Name")
    
    # --- YOUR EXISTING FIELDS (KEPT) ---
    district = models.CharField(max_length=100, default="Seoni", verbose_name="District")
    branch = models.CharField(max_length=100, default="Main Branch", verbose_name="Branch")
    crop_year = models.CharField(max_length=20, default="2025-26", verbose_name="Crop Year")

    # --- NEW FIELDS FOR REGISTERS (ADDED) ---
    stack_no = models.CharField(max_length=50, blank=True, null=True, help_text="Stack No (Deposit)")
    hamar_labor = models.CharField(max_length=100, blank=True, null=True, help_text="Labor Name")
    truck_number = models.CharField(max_length=20, blank=True, null=True, help_text="Truck No (Delivery)")
    gate_pass = models.CharField(max_length=50, blank=True, null=True, help_text="Gate Pass (Delivery)")
    shortage = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Loss/Shortage")

    # --- STANDARD FIELDS ---
    godown = models.ForeignKey(Godown, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TRANSACTION_TYPES)
    
    bags = models.IntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.type} - {self.bags} bags"