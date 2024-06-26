from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CSVFileForm
from .models import CSVFile
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend

def home(request):
    if request.method == 'POST':
        form = CSVFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('plot')
    else:
        form = CSVFileForm()
    return render(request, 'insighty/home.html', {'form': form})

def plot(request):
    csv_file = CSVFile.objects.last()
    if csv_file:
        data = pd.read_csv(csv_file.file.path)

        # Data cleaning: Ensure all columns are numeric
        data = data.apply(pd.to_numeric, errors='coerce')

        # Drop columns that are completely non-numeric
        data = data.dropna(axis=1, how='all')

        if data.empty:
            return render(request, 'insighty/plot.html', {'data': 'No numeric data to display'})

        # Plotting with Matplotlib
        plt.figure(figsize=(10, 6))
        for column in data.columns:
            plt.plot(data.index, data[column], label=column)

        plt.legend()
        plt.xlabel('Index')
        plt.ylabel('Values')
        plt.title('CSV Data Plot')
        plt.savefig('insighty/static/insighty/plot.png')
        plt.close()  # Close the figure to free memory

        return render(request, 'insighty/plot.html', {'data': data.to_html()})
    else:
        return render(request, 'insighty/plot.html', {'data': 'No data to display'})

@csrf_exempt
def refresh(request):
    return redirect('plot')

@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        CSVFile.objects.all().delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
