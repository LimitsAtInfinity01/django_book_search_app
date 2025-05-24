import requests
from book_data.lo_api_wrapper.wrapper import BookAPI, CoverAPI

from django.core.cache import cache


#Main fetch book data function
def main_fetch(search_term, limit: int = 99):

    search = BookAPI(search_term=search_term, limit=10)
    books = search.get_docs()
    
    book_list = []
    for book in books: # type: ignore

        cover_edition_key = book.get('cover_edition_key', None)
        if cover_edition_key is None:
            cover_url = None
        else:
            cover_url = f'https://covers.openlibrary.org/b/olid/{cover_edition_key}-M.jpg?default=false' 

        dict = {
            "author_key": book.get('author_key', 'N/A'),
            "author_name": book.get('author_name', 'N/A'),
            "first_publish_year": book.get('first_publish_year', 'N/A'),
            "language": book.get('language', 'N/A'),
            "title": book.get('title', 'N/A'),
            "subtitle": book.get('subtitle', 'N/A'),
            'key': book.get('key', None),
            "bookUrl": f'/book_view{book.get('key', None)}/{cover_edition_key}/',
            "cover_url": cover_url
        }
        book_list.append(dict)

    for book in book_list:
        for k, v in book.items():
            print(f'{k}: {v}')

    return book_list


def book_data_reading_list(book_id, cover_key):
    # Try to get data from the cache first
    cache_key = f'book_data_{book_id}'
    book_details = cache.get(cache_key)
    if book_details:
        return book_details

    # Use a persistent session for HTTP requests
    session = requests.Session()

    # Fetch the book details
    api_url = f'https://openlibrary.org/works/{book_id}.json'
    response = session.get(api_url)
    data = response.json()

    # Fetch author details using the author key from book data
    author_key = data['authors'][0]['author']['key']
    author_api = f'https://openlibrary.org/{author_key}.json'
    author_response = session.get(author_api)
    author_full_name = author_response.json()

    # Determine the cover URL
    if cover_key and cover_key != 'null':
        cover_url = f'https://covers.openlibrary.org/b/olid/{cover_key}-M.jpg'
    else:
        cover_url = '/static/images/books.jpeg'

    # Construct the book details dictionary
    book_details = {
        "author_name": author_full_name.get('name', ''),
        "author_key": data.get('authors', [{}])[0].get('author', {}).get('key', ''),
        "description": data.get('description', ''),
        "title": data.get('title', ''),
        "cover": cover_url,
        "subject_places": data.get('subject_places', []),
        "subject_times": data.get('subject_times', []),
        "first_link": data.get('links', [None])[0],
        "first_publish_date": data.get('first_publish_date', ''),
        "book_id": book_id,
        "cover_key": cover_key 
    }

    # Cache the result to improve performance on subsequent requests
    cache.set(cache_key, book_details, 3600)  # Cache for 1 hour

    return book_details


