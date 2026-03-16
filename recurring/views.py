from django.shortcuts import render, redirect
from .models import Recurring
from .forms import RecurringTransactionForm

def add_recurring(request):
    if request.method == 'POST':
        form = RecurringTransactionForm(request.POST)
        if form.is_valid():
            recurring_transaction = form.save(commit=False)
            recurring_transaction.user = request.user
            recurring_transaction.save()
            return redirect('recurring_list')
    else:
        form = RecurringTransactionForm()

    return render(request, 'add_recurring.html', {'form': form})

def view_recurring(request):
    # Retrieve all recurring transactions for the current user
    recurring_transactions = Recurring.objects.filter(user=request.user)
    print(recurring_transactions)
    # Render the 'recurring_list.html' template and pass the recurring transactions as context
    return render(request, 'recurring_list.html', {'recurring_transactions': recurring_transactions})
