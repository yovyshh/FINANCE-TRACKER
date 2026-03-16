from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Expense
from django.db.models.signals import post_save
from django.dispatch import receiver
from budget.models import Budget
from .models import *
from budget.models import Budget
from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from category.models import Category, SubCategory
from django.core.exceptions import ValidationError
from django.db import transaction  # Import for atomic transactions
from django.core.exceptions import ValidationError
from datetime import timedelta

def add_expense(request):
    active_budgets = Budget.objects.filter(
        user=request.user,
        start_date__lte=now().date(),
        expiry_date__gte=now().date()
    )

    if not active_budgets.exists():
        return render(request, 'no_budget.html', {'message': 'No active budget available!'})

    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        selected_budget_ids = request.POST.getlist('budget_ids[]')

        if form.is_valid() and selected_budget_ids:
            expense = form.save(commit=False)
            expense.user = request.user

            try:
                with transaction.atomic():
                    for budget_id in selected_budget_ids:
                        selected_budget = Budget.objects.get(id=budget_id, user=request.user)
                        if selected_budget.remaining_amount is None:
                            selected_budget.remaining_amount = selected_budget.initial_amount

                        if selected_budget.remaining_amount >= expense.amount:
                            selected_budget.remaining_amount -= expense.amount
                            selected_budget.save()

                            expense.budget = selected_budget
                            expense.save()

                            history_entry = BudgetHistory(
                                budget=selected_budget,
                                expense=expense,
                                remaining_balance=selected_budget.remaining_amount
                            )
                            history_entry.save()
                        else:
                            raise ValidationError(f"Insufficient funds in budget '{selected_budget.name}'.")

                    # Handle recurring expenses
                    
                       

            except ValidationError as e:
                return render(request, 'add_expense.html', {
                    'form': form,
                    'budgets': active_budgets,
                    'error': str(e),
                })

            return redirect('list_expense')

    else:
        form = ExpenseForm(user=request.user)

    return render(request, 'add_expense.html', {
        'form': form,
        'budgets': active_budgets,
    })
    
def list_expenses(request):
    expenses = Expense.objects.filter(user=request.user).select_related('category', 'subcategory')
    return render(request, 'list_expense.html', {'expenses': expenses})

def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Retrieve the selected budget linked to the expense
        budget_id = expense.budget.id  # Correctly access the ID of the related Budget
        selected_budget = Budget.objects.get(id=budget_id)
        
        if selected_budget.remaining_amount is None:
            # Initialize the remaining amount if it's None (optional)
            selected_budget.remaining_amount = selected_budget.initial_amount
        
        # Add the expense amount back to the remaining amount
        selected_budget.remaining_amount += expense.amount

        # Save the updated budget
        selected_budget.save()

        # Now delete the expense
        expense.delete()

        return redirect('list_expense')
    
    return render(request, 'delete_expense.html', {'expense': expense})




def get_subcategories(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = SubCategory.objects.filter(category=category,user=request.user)
    data = {'subcategories': [{'id': sub.id, 'name': sub.title} for sub in subcategories]}
    return JsonResponse(data)






def budget_history(request, budget_id):
    if budget_id is None:
        # Show a list of all budgets
        budgets = BudgetHistory.objects.all()
    else:
        # Show history for a specific budget
        budget = get_object_or_404(Budget, id=budget_id)
        budgets = BudgetHistory.objects.filter(budget=budget)  # Correctly filter by budget

    # Ensure that the comparison uses Decimal values for accurate arithmetic
    for history in budgets:
        remaining_amount = Decimal(str(history.budget.remaining_amount))  # Convert to Decimal explicitly
        initial_amount = Decimal(str(history.budget.initial_amount))  # Convert to Decimal explicitly

        # Assign the balance status based on remaining balance
        if remaining_amount <= initial_amount * Decimal('0.1'):
            history.balance_status = 'low-balance'  # Red color
        elif remaining_amount <= initial_amount * Decimal('0.5'):
            history.balance_status = 'medium-balance'  # Yellow color
        else:
            history.balance_status = 'normal-balance'  # Green color

    return render(request, 'budget_history.html', {'budgets': budgets})

