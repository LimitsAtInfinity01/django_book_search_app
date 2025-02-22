from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, user_logged_in
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import requests


from book_data.models import Reviews, Comments, ReadingList
from book_data.forms import ReviewsForm, CommentsForm
from book_data.fetch_book_data import fetch_book_data

# Create your views here.
def index(request):
    return render(request, "book_data/index.html")

@login_required
def user_reading_list(request):
    user = request.user
    reading_list = ReadingList.objects.filter(user=user)

    books = []

    for item in reading_list:
        book_id = item.book_id
        cover_key = item.cover_id

        book = fetch_book_data(book_id, cover_key)
        books.append(book)

    return render(request, 'book_data/user_reading_list.html', { 'books': books })

@login_required
def add_reading_list(request):
    book_details = request.session.get('book_details')  # Use as needed in your logic
    bookID = book_details.get('book_id')
    coverKey = book_details.get('cover_key')
    title = book_details.get('title')

    reading_list, created = ReadingList.objects.get_or_create(
        user = request.user,
        title = title,
        book_id = bookID,
        cover_id = coverKey
    )

    if created:
        print(f'Book with {title} and {bookID} added')
        messages.info(request, 'Book added to reading list!')
    else:
         print(f'Book with {title} and {bookID} not added')


    return redirect(book_view, bookID, coverKey)

def book_view(request, book_id, cover_key):
    api_url = f'https://openlibrary.org/works/{book_id}.json'

    response = requests.get(api_url)
    data = response.json()

    author_key = data['authors'][0]['author']['key']
    author_api = f'https://openlibrary.org/{author_key}.json'
    
    author_response = requests.get(author_api)
    author_full_name = author_response.json()

    if cover_key and cover_key != 'null':
        cover_url = f'https://covers.openlibrary.org/b/olid/{cover_key}-M.jpg'
    else:
        cover_url = '/static/images/books.jpeg'

    desc = data.get('description', '')
    if isinstance(desc, dict):
        description = desc.get('value', '')
    else:
        description = desc

    book_details = {
        "author_name": author_full_name.get('name', ''),  # fallback to empty string if missing
        "author_key": data.get('authors', [{}])[0].get('author', {}).get('key', ''),
        "description": description,
        "title": data.get('title', ''),
        "cover": cover_url,  # Assuming cover_url is always provided
        "subject_places": data.get('subject_places', []),  # fallback to empty list
        "subject_times": data.get('subject_times', []),
        "first_link": data.get('links', [None])[0],  # gets the first link or None
        "first_publish_date": data.get('first_publish_date', ''),
        "book_id": book_id,
        "cover_key": cover_key 
    }

    request.session['book_details'] = book_details

    reviews = Reviews.objects.filter(book_id=book_id)

    all_reviews = []
    for item in reviews:
        reviews_dict = {
            'reviewer': item.reviewer.username,
            'title': item.title,
            'content': item.content,
            'rating': item.rating,
            'review_date': item.review_date
        }

        all_reviews.append(reviews_dict)

    context = {
        'book_details': book_details,
        'reviews': all_reviews
    }
    
    return render(request, 'book_data/book_view.html', context)

@login_required 
def write_review(request):
    book_details = request.session.get('book_details')  # Use as needed in your logic
    bookID = book_details.get('book_id')
    coverKey = book_details.get('cover_key')

    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():

            # Process the validated data
            review_title = form.cleaned_data['title']
            review_content = form.cleaned_data['content']
            review_rating = form.cleaned_data['rating']

            # TODO: Save the review or perform other actions

            review = Reviews(reviewer = request.user,
                             book_id = bookID,
                             title = review_title,
                             content = review_content,
                             rating = review_rating)
            review.save()
            
            # Optionally, redirect to a success page to prevent form re-submission
            return redirect(fetch_book, bookID, coverKey)
    else:
        form = ReviewsForm()
    return render(request, 'book_data/write_review.html', {'form': form})

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

