from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, user_logged_in
import json


from book_data.models import Reviews, Comments, ReadingList
from book_data.forms import ReviewsForm, CommentsForm

# Create your views here.
def index(request):
    return render(request, "book_data/index.html")


def view_book(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            authors_string = ''
            for author in data['author_name']:
                if authors_string == '':
                    authors_string = author
                else:
                    authors_string = authors_string + ', ' + author

            book_info_dict = {
                "title": data.get('title', 'Unknown'),
                "subtitle": data.get('subtitle', 'No subtitle'),
                "cover_edition_id": data.get('cover_edition_key', None),
                "publication_year": data.get('first_publish_year', 'Unknown'),
                "language": data.get('language', 'Unknown'),
                "author": authors_string,
                "author_key": data.get('author_key', 'Unknown'),
                "open_library_work_id": data.get('key', 'Unknown')
            }
            request.session['book_info'] = book_info_dict

            return JsonResponse({'success': True, 'message': 'Data received'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
        
    book_info = request.session.get('book_info', None)
    return render(request, 'book_data/view_book.html', {
        "book_info": book_info, 
        })

def get_data_for_view_book():
    pass


def get_book_info(request):
    book_info = request.session.get('book_info', None)
    if book_info:
        return JsonResponse({'success': True, 'book_info': book_info})
    return JsonResponse({'success': False, 'message': 'No book data found'})


@csrf_exempt
def add_to_reading_list(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # print(data)
            if not request.user.is_authenticated:
                return JsonResponse({'success': False, 'message': 'User not authenticated'}, status=401)

            # Ensure required fields are present
            if 'title' not in data or 'open_library_work_id' not in data:
                return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)

            # Create or check if book is already in the list
            reading_list, created = ReadingList.objects.get_or_create(
                user = request.user,
                author = data['author'],
                defaults={'title': data['title']},
                open_library_id=data['open_library_work_id'],
            )

            # reading_list = ReadingList()
            # reading_list.user = request.user
            # reading_list.author = data['author']
            # reading_list.title = data['title']
            # reading_list.open_library_id = data['open_library_work_id']
            # print(data['open_library_work_id'])
            # reading_list.save()

            if created:
                return JsonResponse({'success': True, 'message': 'Book added successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Book already in list'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

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
