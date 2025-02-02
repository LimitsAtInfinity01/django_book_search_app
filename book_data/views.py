from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, user_logged_in
import json

from book_data.models import Reviews, Comments, ReadingList

# Create your views here.
def index(request):
    return render(request, "book_data/index.html")


@csrf_exempt
def add_to_reading_list(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        
        if request.user.is_authenticated:
            reading_list = ReadingList()
            reading_list.title = data['title']
            reading_list.open_library_id = data['open_library_work_id']
            reading_list.author = request.user
            reading_list.save()
        else:
            return redirect('home')
        

    return JsonResponse({'success': True})


def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    return render(request, 'book_data/login.html', {"form": form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'book_data/register.html', {"form": form})

def logout_view(request):
    logout(request)
    return redirect('index')
