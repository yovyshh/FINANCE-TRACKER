from django.shortcuts import render, redirect
from .models import TaxSlab
from .forms import TaxSlabForm

def add_tax_slab(request):
    if request.method == 'POST':
        form = TaxSlabForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tax_slab_list')  # Redirect to the list page after saving
    else:
        form = TaxSlabForm()

    tax_slabs = TaxSlab.objects.all()  # Fetching all tax slabs
    return render(request, 'add_tax_slab.html', {'form': form, 'tax_slabs': tax_slabs})

def tax_slab_list(request):
    tax_slabs = TaxSlab.objects.all()  # Fetching all tax slabs
    return render(request, 'tax_slab_list.html', {'tax_slabs': tax_slabs})
