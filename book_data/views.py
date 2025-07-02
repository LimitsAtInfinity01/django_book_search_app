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
from django.templatetags.static import static 
import json
import requests

from itertools import chain
from operator import attrgetter


# User model
from django.contrib.auth.models import User

# Models
from book_data.models import Reviews, Comments, ReadingList, Profile, FavoriteBooks, Following, TextPosts, ImagePosts, VideoPosts

# Forms
from book_data.forms import ReviewsForm, CommentsForm, AvatarForm, BioForm, ImagePostForm, VideoPostForm, TextPostForm

# Fetch book data classes
from book_data.fetch_book_data import  main_fetch

# API Wrapper
from book_data.lo_api_wrapper.wrapper import CoverAPI
 

# Create your views here.
def index(request):
    query = request.GET.get('query')
    image_form = ImagePostForm()
    video_form = VideoPostForm()
    text_form = TextPostForm()
    print('Hello')
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'image_form':
            form = ImagePostForm(request.POST, request.FILES)

        elif form_type == 'video_form':
            form = VideoPostForm(request.POST, request.FILES)

        else:
            form = TextPostForm(request.POST, request.FILES)

        if form and form.is_valid():
            post = form.save(commit=False)
            post.post_type = form_type
            post.user = request.user
            post.save()
            return redirect('recent_posts')

    if query:
        books = main_fetch(query)
        context = {
            'books': books,
            'image_form': image_form,
            'video_form': video_form,
            'text_form': text_form,
        }
        return render(request, "book_data/index.html", context)
    
    context = {
        'image_form': image_form,
        'video_form': video_form,
        'text_form': text_form,
    }
    return render(request, "book_data/index.html", context)

# This logic is duplicated in the user profile view
def recent_posts():
    try:
        image_posts = ImagePosts.objects.all().order_by('-created_at')
    except ObjectDoesNotExist:
        image_posts = None

    try:
        video_posts = VideoPosts.objects.all().order_by('-created_at')
    except ObjectDoesNotExist:
        video_posts = None

    try:
        text_posts = TextPosts.objects.all().order_by('-created_at')
    except ObjectDoesNotExist:
        text_posts = None


    all_posts = list(chain(image_posts, video_posts, text_posts))

    all_posts_sorted = sorted(all_posts, key=attrgetter('created_at'), reverse=True)
    return all_posts_sorted

def render_recent_posts(request):

    posts = recent_posts()

    context = {
        'posts': posts
    }

    return render(request, 'book_data/recent_posts.html', context)

@login_required
def follow(request):
    if request.method == 'POST':
        follower = request.user
        following_id = request.POST.get('following_id')
        following = get_object_or_404(User, id=following_id)
        print("Before")
        if follower != following:
            # Create relation only if it doesn't exist
            print("After")
            Following.objects.get_or_create(follower=follower, following=following)

        next_url = request.POST.get('next', '/')
        return redirect(next_url)

def favorite_books(request, book_id, cover_key=None):
    book_details = request.session.get('book_details', {})  # Ensure a default empty dict
    title = book_details.get('title', 'Unknown Title')

    cover_url = f'https://covers.openlibrary.org/b/olid/{cover_key}.jpg'
    favorites_books, created = FavoriteBooks.objects.get_or_create(
        user=request.user,
        title=title,
        book_id=book_id,
        cover_url=cover_url,
        cover_id=cover_key
    )

    next_url = request.GET.get('next') or request.POST.get('next')

    if created:
        messages.success(request, 'Book added to favorites!')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(reverse('book_view', args=[book_id, cover_key]))
    else:
        messages.error(request, 'Book already in favorites!')
        return redirect(reverse('book_view', args=[book_id, cover_key]))

def favorite_books_list(request):
    try:
        books = FavoriteBooks.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        books = None

    context = {
        'books': books
    }

    return render(request, 'book_data/favorite_books.html', context)

@login_required
def user_profile_page(request, user_id):
    if request.method == 'POST':
        if 'submit_avatar' in request.POST:
            avatar_form = AvatarForm(request.POST, request.FILES)
            bio_form = BioForm()  # empty form
            if avatar_form.is_valid():
                profile = request.user.profile
                profile.avatar = avatar_form.cleaned_data['avatar']
                profile.save()
                return redirect('user_profile_page', user_id)
        elif 'submit_bio' in request.POST:
            bio_form = BioForm(request.POST)
            avatar_form = AvatarForm()  # empty form
            if bio_form.is_valid():
                profile = request.user.profile
                profile.bio = bio_form.cleaned_data['bio']
                profile.save()
                return redirect('user_profile_page', user_id)
    else:
        avatar_form = AvatarForm()
        bio_form = BioForm()
        
    try:
        profile = request.user.profile
        avatar_url = profile.avatar.url
    except ObjectDoesNotExist:
        avatar_url = None        

    try:
        profile = request.user.profile
        bio = profile.bio
    except ObjectDoesNotExist:
        bio = None

    try: 
        reading_list = ReadingList.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        reading_list = None

    try:
        reviews = Reviews.objects.filter(reviewer=request.user).order_by('-created_at')[:10]
    except ObjectDoesNotExist:
        reviews = None

    try: 
        favorite_books = FavoriteBooks.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        favorite_books = None

    try:
        following = Following.objects.filter(follower=request.user).order_by('-created_at')
    except ObjectDoesNotExist:
        following = None
    
    try:
        followers = Following.objects.filter(following=request.user).order_by('-created_at')
    except ObjectDoesNotExist:
        followers = None

    posts = recent_posts()

    context = {
        'reading_list': reading_list,
        'reviews': reviews,
        'favorite_books': favorite_books,
        'avatar_form': avatar_form,
        'avatar_url': avatar_url,
        'bio': bio,
        'following': following,
        'followers': followers,
        'bio_form': bio_form, 
        'posts': posts
    }

    print(f'Followers: {followers}')
    print(f'Following: {following}')

    return render(request, 'book_data/user_profile_page.html', context)

def general_profile_page(request, user_id):

    user = User.objects.get(id=user_id)
    profile = user.profile

    try:
        avatar_url = profile.avatar.url
    except ObjectDoesNotExist:
        avatar_url = None        

    try:
        bio = profile.bio
    except ObjectDoesNotExist:
        bio = None

    try: 
        reading_list = ReadingList.objects.filter(user=profile.user)
    except ObjectDoesNotExist:
        reading_list = None

    try:
        reviews = Reviews.objects.filter(reviewer=profile.user).order_by('-created_at')[:10]
    except ObjectDoesNotExist:
        reviews = None

    try: 
        favorite_books = FavoriteBooks.objects.filter(user=profile.user)
    except ObjectDoesNotExist:
        favorite_books = None

    try:
        following = Following.objects.filter(follower=profile.user).order_by('-created_at')
    except ObjectDoesNotExist:
        following = None
    
    try:
        followers = Following.objects.filter(following=profile.user).order_by('-created_at')
    except ObjectDoesNotExist:
        followers = None

    
    context = {
        'user': user,
        'user_id': user_id,
        'reading_list': reading_list,
        'reviews': reviews,
        'favorite_books': favorite_books,
        'avatar_url': avatar_url,
        'bio': bio,
        'following': following,
        'followers': followers
    }

    return render(request, 'book_data/general_profile_page.html', context)

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
def delete_post(request, post_id):

    # Get the type of the post and delete it
    if request.method == 'POST':
        print(request.POST)
        if 'post' in request.POST:
            if request.POST['post'] == 'image':
                post = get_object_or_404(ImagePosts, id=post_id)

            if request.POST['post'] == 'video':
                post = get_object_or_404(VideoPosts, id=post_id)
            
            if request.POST['post'] == 'text':
                post = get_object_or_404(TextPosts, id=post_id)
                
            if request.user == post.user:
                post.delete()
                return redirect('recent_posts')
            



    return redirect('recent_posts')

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

def reviews_page(request):
    
    try:
        reviews = Reviews.objects.all().order_by('-created_at')
    except ObjectDoesNotExist:
        reviews = None
    
    context = {
        'reviews': reviews
    }

    return render(request, 'book_data/reviews_page.html', context)

@login_required
def user_reading_list(request):
    user = request.user
    reading_list = ReadingList.objects.filter(user=user)
    books = []

    for item in reading_list:
        cover = CoverAPI(value=item.cover_id)
        cover_url = cover.get_image()
        book = {
            'book_id': item.book_id,
            'cover_key': item.cover_id,
            'title': item.title,
            'author_name': item.author_name,
            'cover_url': cover_url
        }
        books.append(book)
    return render(request, 'book_data/user_reading_list.html', { 'books': books })

@login_required
def add_reading_list(request, book_id, cover_key=None):
    book_details = request.session.get('book_details', {})  # Ensure a default empty dict
    title = book_details.get('title', 'Unknown Title')
    author_name = book_details.get('author_name', 'Unknown Author')
    reading_list, created = ReadingList.objects.get_or_create(
        user=request.user,
        title=title,
        author_name=author_name,
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

    # Check for non-200 status
    if response.status_code != 200:
        print("API returned non-200 status:", response.status_code)
        print("Response text:", response.text)
        return HttpResponse("Error: Failed to fetch data from API", status=500)

    # Ensure there's content to decode
    try:
        data = response.json()
    except ValueError as e:
        print("Error decoding JSON:", e)
        print("Response text:", response.text)
        return HttpResponse("Error: Invalid JSON received from API", status=500)


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

    profiles = []
    for review in reviews:
        profile = review.reviewer.profile
        profiles.append(profile)


    for profile in profiles:
            print(profile.user.id)


    context = {
        'book_details': book_details,
        'reviews': reviews,
        'profiles': profiles
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

    cover_url = f'https://covers.openlibrary.org/b/olid/{coverKey}.jpg'
    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():

            review_content = form.cleaned_data['content']
            review_rating = form.cleaned_data['rating']

            # TODO: Save the review or perform other actions

            review = Reviews(reviewer = request.user,
                             book_title=title,
                             book_id = bookID,
                             cover_id = coverKey,
                             cover_url = cover_url,
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