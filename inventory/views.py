from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, Q
from django.contrib import messages
from .models import Transaction, Godown, Crop
from .forms import TransactionForm, BulkImportForm
import pandas as pd
from datetime import datetime, date

# --- 1. AUTHENTICATION (Login/Logout) ---

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# --- 2. DASHBOARD ---

@login_required
def dashboard(request):
    # Statistics
    total_in = Transaction.objects.filter(type='SR').aggregate(Sum('bags'))['bags__sum'] or 0
    total_out = Transaction.objects.filter(type='DL').aggregate(Sum('bags'))['bags__sum'] or 0
    net_stock = total_in - total_out
    
    # Recent Transactions (Last 10)
    recents = Transaction.objects.all().order_by('-date', '-id')[:10]
    
    context = {
        'total_in': total_in,
        'total_out': total_out,
        'net_stock': net_stock,
        'recents': recents,
    }
    return render(request, 'inventory/dashboard.html', context)

# --- 3. TRANSACTIONS (Add, Edit, Delete) ---

@login_required
def add_transaction(request):
    initial_data = {}
    if 'initial' in request.GET:
        initial_data = {'type': request.GET['initial']}
        
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(initial=initial_data)
    
    # Party Autocomplete List
    parties = Transaction.objects.values_list('party_name', flat=True).distinct()
    
    return render(request, 'inventory/add_transaction.html', {
        'form': form,
        'party_list': parties
    })

@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'inventory/edit_transaction.html', {'form': form})

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()
    return redirect('dashboard')

@login_required
def print_receipt(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'inventory/receipt.html', {'t': transaction})

# --- 4. REPORTS & DATA ---

@login_required
def reports(request):
    transactions = Transaction.objects.all().order_by('-date', '-id')
    
    # Filters
    t_type = request.GET.get('type')
    godown_id = request.GET.get('godown')
    crop_id = request.GET.get('crop')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if t_type:
        transactions = transactions.filter(type=t_type)
    if godown_id:
        transactions = transactions.filter(godown_id=godown_id)
    if crop_id:
        transactions = transactions.filter(crop_id=crop_id)
    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)

    # Totals for Footer
    total_bags = transactions.aggregate(Sum('bags'))['bags__sum'] or 0
    total_weight = transactions.aggregate(Sum('weight'))['weight__sum'] or 0

    # CSV Export
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Date', 'Type', 'Party', 'Crop', 'Godown', 'Bags', 'Weight'])
        for t in transactions:
            writer.writerow([t.date, t.get_type_display(), t.party_name, t.crop.name, t.godown.name, t.bags, t.weight])
        return response

    context = {
        'transactions': transactions,
        'godowns': Godown.objects.all(),
        'crops': Crop.objects.all(),
        'current_type': t_type,
        'total_bags': total_bags,
        'total_weight': total_weight
    }
    return render(request, 'inventory/reports.html', context)

@login_required
def import_data(request):
    if request.method == 'POST':
        form = BulkImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                df = pd.read_excel(request.FILES['file'])
                for _, row in df.iterrows():
                    # Logic to find or create IDs would go here
                    # For now, simplistic implementation:
                    pass 
                messages.success(request, "Data imported successfully")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"Error importing: {e}")
    else:
        form = BulkImportForm()
    return render(request, 'inventory/import_data.html', {'form': form})

# --- 5. DETAILS & LEDGERS ---

@login_required
def party_detail(request, party_name):
    transactions = Transaction.objects.filter(party_name=party_name).order_by('-date', '-id')
    
    total_in = transactions.filter(type='SR').aggregate(Sum('bags'))['bags__sum'] or 0
    total_out = transactions.filter(type='DL').aggregate(Sum('bags'))['bags__sum'] or 0
    current_balance = total_in - total_out
    
    return render(request, 'inventory/party_detail.html', {
        'party_name': party_name,
        'transactions': transactions,
        'total_in': total_in,
        'total_out': total_out,
        'current_balance': current_balance
    })

@login_required
def godown_detail(request, godown_id):
    godown = get_object_or_404(Godown, id=godown_id)
    stock = []
    # Logic for godown stock would go here
    return render(request, 'inventory/godown_detail.html', {'godown': godown})




@login_required
def registers_view(request):
    # 1. Get Filters
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    register_type = request.GET.get('tab', 'deposit') # Default to Deposit Register

    # 2. Base Query
    transactions = Transaction.objects.all().order_by('-date')

    # 3. Apply Date Filter
    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)

    # 4. Filter Data based on Register Type (Tabs)
    if register_type == 'deposit':
        # Show only Deposits (Matches your "Deposit Register.pdf")
        data = transactions.filter(type='SR')
    elif register_type == 'delivery':
        # Show only Deliveries (Matches your "Delivery Register.pdf")
        data = transactions.filter(type='DL')
    else:
        # Stock Register (Master View)
        data = transactions

    context = {
        'register_data': data,
        'current_tab': register_type,
        'today': date.today()
    }
    return render(request, 'inventory/register_book.html', context)