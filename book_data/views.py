from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, user_logged_in
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
import json
import requests


from book_data.models import Reviews, Comments, ReadingList, Avatar, Biography
from book_data.forms import ReviewsForm, CommentsForm, BiographyForm #ProfileUpload
from book_data.fetch_book_data import book_data_reading_list, main_fetch

# Create your views here.
def index(request):
    query = request.GET.get('query')
    if query:
        books = main_fetch(query)
        books = books[0:20]
        return render(request, "book_data/index.html", {'books': books})
    return render(request, "book_data/index.html")

def user_profile_page(request):
    # Get the avatar url from database
    try:
        avatar_url = Avatar.objects.filter(user=request.user.id).latest('created_at') 
    except ObjectDoesNotExist:
        avatar_url = None
    
    # Gets the current biography from database
    try:
        current_biography = Biography.objects.filter(user=request.user.id).latest('create_at') 
    except ObjectDoesNotExist:
        current_biography = None

    try: 
        reading_list = ReadingList.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        reading_list = None

    try:
        reviews = Reviews.objects.filter(reviewer=request.user).order_by('-created_at')[:2]
    except ObjectDoesNotExist:
        reviews = None

    print(reviews)    
    for review in reviews:
        print(review.created_at)
    context = {
        'avatar_url': avatar_url,
        'current_biography': current_biography,
        'reading_list': reading_list,
        'reviews': reviews
    }
    return render(request, 'book_data/user_profile_page.html', context)

@login_required
def biography(request):
    if request.method == 'POST':
        form = BiographyForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            biography = Biography(user=request.user,
                                  text=text)
            biography.save()
            return redirect('user_profile_page')
    else:
        form = BiographyForm()

    context = {
        'form': form
    }

    return render(request, 'book_data/biography.html', context)

@login_required
def change_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('avatar_picture'):
        uploaded_avatar = request.FILES['avatar_picture']
        avatar = uploaded_avatar
        fs = FileSystemStorage()
        filename = fs.save(f'avatars/{avatar.name}', avatar)
        avatar_url = fs.url(filename)

        avatar = Avatar(user=request.user,
                            avatar_url=avatar_url)
        
        avatar.save()
        return redirect('user_profile_page')

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
def add_reading_list(request, book_id, cover_key=None):
    book_details = request.session.get('book_details', {})  # Ensure a default empty dict
    title = book_details.get('title', 'Unknown Title')
    print(title)
    reading_list, created = ReadingList.objects.get_or_create(
        user=request.user,
        title=title,
        book_id=book_id,
        cover_id=cover_key
    )

    next_url = request.GET.get('next') or request.POST.get('next')

    if created:
        messages.success(request, 'Book added to reading list!')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(reverse('book_view', args=[book_id, cover_key]))
    else:
        messages.error(request, 'Book already in the list!')
        return redirect(reverse('book_view', args=[book_id, cover_key]))

  
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

    try:
        avatar_url = Avatar.objects.filter(user=request.user.id).latest('created_at')
    except ObjectDoesNotExist:
        avatar_url = None

    context = {
        'book_details': book_details,
        'reviews': reviews,
        'avatar_url': avatar_url
    }
    
    request.session['current_book_id'] = book_id
    request.session['current_cover_key'] = cover_key
    return render(request, 'book_data/book_view.html', context)

@login_required 
def write_review(request):
    book_details = request.session.get('book_details')  # Use as needed in your logic
    bookID = book_details.get('book_id')
    coverKey = book_details.get('cover_key')
    title = book_details.get('title')

    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():

            # Process the validated data
            # review_title = form.cleaned_data['title']
            review_content = form.cleaned_data['content']
            review_rating = form.cleaned_data['rating']

            # TODO: Save the review or perform other actions

            review = Reviews(reviewer = request.user,
                             book_title=title,
                             book_id = bookID,
                             cover_id = coverKey,
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

