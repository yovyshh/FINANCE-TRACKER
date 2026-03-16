from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Sum
from .forms import IncomeForm
from .models import Income, SubCategory
from category.models import Category

from django.http import JsonResponse
from .models import  Income
from expense.models import  Expense
from budget.models import  Budget
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models import Sum, Q
import logging
import json
from taxslab.models import TaxSlab
from django.utils import timezone
logger = logging.getLogger(__name__)

from datetime import datetime, timedelta
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST, user=request.user)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('income_list')
    else:
        form = IncomeForm(user=request.user)

    return render(request, 'add_income.html', {'form': form})



def get_subcategories(request, category_id):
    """
    API endpoint to fetch subcategories based on a given category ID.
    """
    subcategories = SubCategory.objects.filter(category_id=category_id)
    data = {
        'subcategories': [{'id': sub.id, 'name': sub.title} for sub in subcategories]
    }
    return JsonResponse(data)


def income_list(request):
    """
    View to list all incomes for the current user and calculate the total income.
    """
    incomes = Income.objects.filter(user=request.user)  # Fetch incomes for the logged-in user
    total_income = incomes.aggregate(total=Sum('amount'))['total']  # Calculate the total income

    return render(request, 'income_list.html', {
        'incomes': incomes,
        'total_income': total_income
    })
    
   
def delete_income(request, income_id):
    try:
        income = Income.objects.get(id=income_id)
        if income.user == request.user:  # Ensure the user owns the income record
            income.delete()
    except Income.DoesNotExist:
        # Handle the case where the income doesn't exist (optional)
        pass
    return redirect('income_list')  



@login_required
def report_view(request):
    """Render the report page for the logged-in user."""
    current_year = datetime.now().year
    years = list(range(2020, current_year + 1))  # Change starting year as needed

    # Get current month and year
    current_date = timezone.now()
    current_month = current_date.month
    current_year = current_date.year

    # Fetch Budget objects for the logged-in user
    budgets = Budget.objects.filter(user=request.user)

    # Get filtered expense data for the current month
    expenses = Expense.objects.filter(user=request.user, date__year=current_year, date__month=current_month)
    
    # Get filtered income data for the current month
    incomes = Income.objects.filter(user=request.user, created_at__year=current_year, created_at__month=current_month)
    
    # Calculate total income, total expense, and balance income for the current month
    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0
    balance_income = total_income - total_expense
    
    context = {
        'years': years,
        'budgets': budgets,
        'expenses': expenses,
        'incomes': incomes,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance_income': balance_income,
    }
    
    return render(request, 'user_report.html', context)


@login_required
def filter_data(request):
    # Retrieve filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    year = request.GET.get('year')
    data_type = request.GET.get('dataType')

    # Get current month and year
    current_date = timezone.now()
    current_month = current_date.month
    current_year = current_date.year

    # Initialize queryset based on data type
    if data_type == 'expense':
        data = Expense.objects.filter(user=request.user)
        fields = ['title', 'description', 'amount', 'category__title', 'subcategory__title', 'budget__name', 'date']
    elif data_type == 'income':
        data = Income.objects.filter(user=request.user)
        fields = ['title', 'description', 'amount', 'category__title', 'subcategory__title', 'created_at']
    else:
        data = Expense.objects.filter(user=request.user) | Income.objects.filter(user=request.user)
        fields = ['title', 'description', 'amount', 'category__title', 'subcategory__title', 'budget__name', 'date']

    # Apply chosen filters
    if start_date:
        try:
            parsed_start_date = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            if end_date:
                parsed_end_date = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
            else:
                parsed_end_date = timezone.now()
            if data_type == 'budget':
                data = data.filter(start_date__range=(parsed_start_date, parsed_end_date))
            elif data_type == 'income':
                data = data.filter(created_at__range=(parsed_start_date, parsed_end_date))
            else:
                data = data.filter(date__range=(parsed_start_date, parsed_end_date))
        except ValueError:
            print("Invalid date format")

    if year:
        try:
            start_year = int(year)
            fiscal_start_date = timezone.make_aware(datetime(start_year, 4, 1))
            fiscal_end_date = timezone.make_aware(datetime(start_year + 1, 3, 31))
            if data_type == 'budget':
                data = data.filter(start_date__range=(fiscal_start_date, fiscal_end_date))
            elif data_type == 'income':
                data = data.filter(created_at__range=(fiscal_start_date, fiscal_end_date))
            elif data_type == 'expense':
                data = data.filter(date__range=(fiscal_start_date, fiscal_end_date))
            else:
                data = data.filter(date__range=(fiscal_start_date, fiscal_end_date))
        except ValueError:
            print("Invalid year format")

    # Calculate totals and balances for filtered data
    if data_type == 'expense':
        total_income = Income.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
        total_expense = data.aggregate(total=Sum('amount'))['total'] or 0
        balance_income = total_income - total_expense
    elif data_type == 'income':
        total_income = data.aggregate(total=Sum('amount'))['total'] or 0
        total_expense = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
        balance_income = total_income - total_expense
    else:
        total_income = Income.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
        total_expense = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
        balance_income = total_income - total_expense

    # Prepare response data
    response_data = {
        'current_month': {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance_income': balance_income,
        },
        'filtered_data': {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance_income': balance_income,
        },
        'data': list(
            data.values(*fields)
            .annotate(amount_sum=Sum('initial_amount' if data_type == 'budget' else 'amount'))
            .order_by('-amount_sum')
        ),
    }

    return JsonResponse(response_data)




















@login_required
def filter_superuser_categories(request):
    # Get current date and month
    current_date = timezone.now()
    current_month = current_date.month
    current_year = current_date.year
    
    # Filter categories by superuser or current user, and filter expenses by the current month
    categories = Category.objects.filter(
        Q(user__is_superuser=True) | Q(user=request.user)
    ).annotate(
        total_expenses=Sum('expenses__amount')
    )
    
    # Filter expenses based on the current month
    categories = categories.filter(
        expenses__date__month=current_month,
        expenses__date__year=current_year
    ).order_by('title')
    
    category_data = categories.values('id', 'title', 'user__username').annotate(
        total_expenses=Sum('expenses__amount')
    ).order_by('title')

    response_data = [
        {
            'id': category['id'],
            'title': category['title'],
            'creator': category['user__username'],
            'total_expenses': category['total_expenses'] or 0
        }
        for category in category_data
    ]

    return JsonResponse({'categories': response_data})

# @login_required
# def common_report(request):
#     current_year = datetime.now().year
#     years = list(range(2020, current_year + 1))

#     # Calculate totals for the current year
#     incomes = Income.objects.filter(user=request.user, created_at__year=current_year, category__user__isnull=True)
#     expenses = Expense.objects.filter(user=request.user, date__year=current_year, category__user__isnull=True)
#     total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
#     total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
#     balance = total_income - total_expense

#     # Determine the applicable tax slab
#     applicable_tax_slab = TaxSlab.objects.filter(min_limit__lte=balance, max_limit__gte=balance).first()
#     tax_percentage = applicable_tax_slab.tax_percentage if applicable_tax_slab else 0
#     tax_amount = (total_income * tax_percentage / 100) if applicable_tax_slab else 0

#     return render(request, 'common_report.html', {
#         'years': years,
#         'total_income': total_income,
#         'total_expense': total_expense,
#         'balance': balance,
#         'tax_percentage': tax_percentage,
#         'tax_amount': tax_amount
#     })




@login_required
def common_report(request):
    current_year = datetime.now().year
    years = list(range(2020, current_year + 1))

    # Calculate totals for the current year
    incomes = Income.objects.filter(category__user__is_superuser=True, created_at__year=current_year)
    print("Incomes:", incomes)
    expenses = Expense.objects.filter(category__user__is_superuser=True, date__year=current_year)
    print("Expenses:", expenses)
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    print("Total Income:", total_income)
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    print("Total Expense:", total_expense)
    balance = total_income - total_expense
    print("Balance:", balance)

    # Determine the applicable tax slab
    applicable_tax_slab = TaxSlab.objects.filter(min_limit__lte=balance, max_limit__gte=balance).first()
    print("Applicable Tax Slab:", applicable_tax_slab)
    tax_percentage = applicable_tax_slab.tax_percentage if applicable_tax_slab else 0
    print("Tax Percentage:", tax_percentage)
    tax_amount = (total_income * tax_percentage / 100) if applicable_tax_slab else 0
    print("Tax Amount:", tax_amount)

    return render(request, 'common_report.html', {
        'years': years,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'tax_percentage': tax_percentage,
        'tax_amount': tax_amount
    })



from django.db.models import F
from django.db.models import Sum

@login_required
def fetch_common_report_data(request):
    year = request.GET.get('year')
    print(f"Year received in request: {year}")

    start_month = 4  # Default fiscal year start (April)
    end_month = 3  # Default fiscal year end (March)

    if year:
        try:
            start_year = int(year.split('-')[0])
            fiscal_start_date = timezone.make_aware(datetime(start_year, start_month, 1))
            fiscal_end_year = start_year + 1 if start_month > end_month else start_year
            fiscal_end_date = timezone.make_aware((datetime(fiscal_end_year, end_month, 1) + timedelta(days=31)).replace(day=1) - timedelta(days=1))
        except ValueError:
            print("Invalid year format in request.")
            return JsonResponse({'error': 'Invalid year format'}, status=400)
    else:
        current_date = timezone.now()
        fiscal_start_date = timezone.make_aware(datetime(current_date.year, start_month, 1))
        fiscal_end_date = timezone.make_aware((datetime(current_date.year + 1, end_month, 1) + timedelta(days=31)).replace(day=1) - timedelta(days=1))

    print(f"Fiscal Start Date: {fiscal_start_date}, Fiscal End Date: {fiscal_end_date}")

    # Filter data
    expenses = Expense.objects.filter(
        category__user__is_superuser=True,
        date__range=(fiscal_start_date, fiscal_end_date)
    )
    incomes = Income.objects.filter(
        category__user__is_superuser=True,
        created_at__range=(fiscal_start_date, fiscal_end_date)
    )

    print(f"Filtered Expenses: {expenses}")
    print(f"Filtered Incomes: {incomes}")

    # Aggregate data grouped by category and subcategory
    expense_data = (
        expenses.values(
            category_title=F('category__title'),
            subcategory_title=F('subcategory__title')
        )
        .annotate(total_amount=Sum('amount'))
        .order_by('category_title', 'subcategory_title')
    )
    income_data = (
        incomes.values(
            category_title=F('category__title'),
            subcategory_title=F('subcategory__title')
        )
        .annotate(total_amount=Sum('amount'))
        .order_by('category_title', 'subcategory_title')
    )

    print(f"Aggregated Expense Data: {list(expense_data)}")
    print(f"Aggregated Income Data: {list(income_data)}")

    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    print(f"Total Income: {total_income}, Total Expense: {total_expense}, Balance: {balance}")

    # Determine applicable tax slab
    applicable_tax_slab = TaxSlab.objects.filter(min_limit__lte=balance, max_limit__gte=balance).first()
    tax_percentage = applicable_tax_slab.tax_percentage if applicable_tax_slab else 0
    tax_amount = (total_income * tax_percentage / 100) if applicable_tax_slab else 0

    print(f"Applicable Tax Slab: {applicable_tax_slab}, Tax Percentage: {tax_percentage}, Tax Amount: {tax_amount}")

    response_data = {
        'expenses': list(expense_data),
        'incomes': list(income_data),
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'tax_percentage': tax_percentage,
        'tax_amount': tax_amount,
    }

    print(f"Response Data: {response_data}")
    return JsonResponse(response_data)



    
@login_required
def filter_categories(request):
    category_id = request.GET.get('category_id')

    if category_id:
        # Filter expenses by the selected category
        categories = Category.objects.filter(id=category_id).annotate(
            total_expenses=Sum('expenses__amount')
        )
    else:
        # Fetch all categories with their total expenses
        categories = Category.objects.annotate(
            total_expenses=Sum('expenses__amount')
        )

    data = [
        {
            'id': category.id,
            'title': category.title,
            'creator': category.user.username if category.user else 'Unknown',
            'total_expenses': category.total_expenses or 0
        }
        for category in categories
    ]

    return JsonResponse({'categories': data})