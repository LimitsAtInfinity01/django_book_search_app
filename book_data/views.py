from django.shortcuts import render, redirect, get_object_or_404
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
from book_data.fetch_book_data import book_data_reading_list, main_fetch

# Create your views here.
def index(request):
    
    if request.method == "POST":
        query = request.POST.get('query')

        if query == '':
            return redirect('index')
        else:
            books = main_fetch(query)

            books = books[0:21]
            return render(request, "book_data/index.html", { 'books': books })
        
    return render(request, "book_data/index.html")

def delete_review_from_list(request, review_id):
    review = get_object_or_404(Reviews, id=review_id)
    if request.user == review.reviewer:
        if request.method == 'POST':
            review.delete()
            return redirect('user_reviews_page')



@login_required
def delete_review(request, review_id):
    current_book_id = request.session.get('current_book_id')
    current_cover_key = request.session.get('current_cover_key')

    review = get_object_or_404(Reviews, id=review_id)
    print(review_id)

    if request.user == review.reviewer:
        if request.method == 'POST':
            review.delete()
            return redirect('book_view', current_book_id, current_cover_key)

    return redirect('book_view', current_book_id, current_cover_key)


@login_required
def get_comment(request, review_id):
    
    current_book_id = request.session.get('current_book_id')
    current_cover_key = request.session.get('current_cover_key')

    review = Reviews.objects.get(id=review_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        print(content)
        comment = Comments(reviews=review,
                           author=request.user,
                           content=content)
        comment.save()

        return redirect('book_view', current_book_id, current_cover_key) 

@login_required
def delete_comment(request, comment_id):
    current_book_id = request.session.get('current_book_id')
    current_cover_key = request.session.get('current_cover_key')
    comment = get_object_or_404(Comments, id=comment_id)

    if request.user == comment.author:
        if request.method == 'POST':
            comment.delete()
            return redirect('book_view', current_book_id, current_cover_key)
    else:
        return redirect('login')

def user_reviews_page(request):
    reviews = Reviews.objects.filter(reviewer=request.user.id)

    context = {
        'reviews': reviews
    }
    return render(request, 'book_data/user_reviews.html', context)

@login_required
def user_reading_list(request):
    user = request.user
    reading_list = ReadingList.objects.filter(user=user)

    books = []

    for item in reading_list:
        book_id = item.book_id
        cover_key = item.cover_id

        book = book_data_reading_list(book_id, cover_key)
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
        messages.success(request, 'Book added to reading list!')
    else:
         messages.error(request, 'Book already in the list!')
         print(f'Book with {title} and {bookID} not added')


    return redirect(book_view, bookID, coverKey)

def remove_from_reading_list(request, book_id):
    book = get_object_or_404(ReadingList, book_id=book_id, user=request.user)
    book.delete()
    return redirect('user_reading_list')

def book_view(request, book_id, cover_key=''):
    api_url = f'https://openlibrary.org/works/{book_id}.json'

    response = requests.get(api_url)
    data = response.json()

    author_key = data['authors'][0]['author']['key']
    author_api = f'https://openlibrary.org/{author_key}.json'
    
    author_response = requests.get(author_api)
    author_full_name = author_response.json()

    if cover_key and cover_key != '':
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

    context = {
        'book_details': book_details,
        'reviews': reviews,
    }
    
    request.session['current_book_id'] = book_id
    request.session['current_cover_key'] = cover_key
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
            return redirect(book_view, bookID, coverKey)
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

