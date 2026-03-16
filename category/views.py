from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from .forms import CategoryForm
from .models import  SubCategory
from .forms import SubCategoryForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import ProtectedError
from user_app.models import*

# View to display all categories
def view_category(request):
    # Retrieve categories and filter based on user type and ownership
    ad_categories = Category.objects.filter(user__usertype=1)
    print( ad_categories,"adddddddd")
    # Check if the user is a regular user (usertype == 0) to show only their categories
    if request.user.usertype == 0:
        categories = categories.filter(user=request.user)
        print(categories,"catt")
    return render(request, 'view_category.html', {
        'categories': categories,
        'ad_categories':ad_categories
    })

# View to add a new category
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user  # Assign the current user
            category.save()
            return redirect('view_categories')
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})

# View to edit a category
# views.py
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('view_categories')  # Redirect to category list after saving
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form, 'category': category})

# views.py
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('view_categories')  # Redirect to category list after deletion
    return render(request, 'delete_category.html', {'category': category})




def view_categories(request):
    categories=None
    ad_categories = Category.objects.filter(user__usertype=1)
    print( ad_categories,"adddddddd")
    # Check if the user is a regular user (usertype == 0) to show only their categories
    if request.user.usertype == 0:
        categories = Category.objects.filter(user=request.user)
        print(categories,"catt")
    return render(request, 'view_categories.html', {
        'categories': categories,
        'ad_categories':ad_categories
    })

# View to add a new subcategory under a category
def view_subcategories(request, category_id):
    # Get the specific category or return a 404 if it doesn't exist
    category = get_object_or_404(Category, id=category_id)

    # Fetch only the subcategories belonging to this category
    subcategories = SubCategory.objects.filter(category=category)

    # Handle form submission for adding a new subcategory
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            new_subcategory = form.save(commit=False)
            new_subcategory.category = category  # Assign the current category
            new_subcategory.save()
            # Redirect or render with success message
            return redirect('view_categories')
    else:
        form = SubCategoryForm()

    # Render the template with the category, subcategories, and form
    return render(request, 'add_subcategory.html', {
        'category': category,
        'subcategories': subcategories,
        'form': form
    })
def edit_subcategory(request, subcategory_id):
    try:
        # Try to fetch the subcategory, if not found, it will raise a 404 error
        subcategory = SubCategory.objects.get(id=subcategory_id)
    except SubCategory.DoesNotExist:
        # Log the error or handle the case when the subcategory doesn't exist
        return render(request, 'edit_subcategory.html.html', {'error': f"SubCategory with ID {subcategory_id} not found."})

    if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('view_categories')  # Redirect after save
    else:
        form = SubCategoryForm(instance=subcategory)
    
    return render(request, 'edit_subcategory.html', {'form': form, 'subcategory': subcategory})


def delete_subcategory(request, subcategory_id):
    # Attempt to get the subcategory or handle the error
    subcategory = get_object_or_404(SubCategory, pk=subcategory_id)

    # If it's a POST request, delete the subcategory
    if request.method == 'POST':
        subcategory.delete()
        return redirect('view_categories')  # Redirect after deletion

    # Render the confirmation page with the subcategory data
    return render(request, 'delete_subcategory.html', {'subcategory': subcategory})
