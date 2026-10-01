from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html',{'name': 'Akshay'})

def add(request):
    if request.method == 'POST':
        try:
            val1 = float(request.POST.get('num1', 0))
            val2 = float(request.POST.get('num2', 0))
            res = val1 + val2
            # Clean up display if whole number
            if res.is_integer():
                res = int(res)
            return render(request, 'result.html', {'result': res})
        except ValueError:
            return render(request, 'result.html', {'result': 'Invalid number input'})
    return render(request, 'home.html', {'name': 'Akshay'})
