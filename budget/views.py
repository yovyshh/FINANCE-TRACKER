from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from .models import Budget
from .forms import BudgetForm
from django.views.generic.edit import DeleteView



class BudgetListView(ListView):
    model = Budget
    template_name = 'budget_list.html'
    context_object_name = 'budgets'
    def get_queryset(self):
        """
        Filter the budgets to only include those created by the logged-in user.
        """
        return Budget.objects.filter(user=self.request.user)

class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budget_form.html'
    success_url = reverse_lazy('budget_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Ensure the logged-in user is assigned
        return super().form_valid(form)

class BudgetUpdateView(UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budget_form.html'
    success_url = reverse_lazy('budget_list')

class BudgetDetailView(DetailView):
    model = Budget
    template_name = 'budget_detail.html'
    context_object_name = 'budget'

class BudgetDeleteView(DeleteView):
    model = Budget
    template_name = 'budget_delete.html'  # Template for confirmation
    success_url = reverse_lazy('budget_list')
