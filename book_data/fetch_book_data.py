import requests
import json

def fetch_book_data(book_id, cover_key):
    
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

    book_details = {
        "author_name": author_full_name.get('name', ''),  # fallback to empty string if missing
        "author_key": data.get('authors', [{}])[0].get('author', {}).get('key', ''),
        "description": data.get('description', ''),
        "title": data.get('title', ''),
        "cover": cover_url,  # Assuming cover_url is always provided
        "subject_places": data.get('subject_places', []),  # fallback to empty list
        "subject_times": data.get('subject_times', []),
        "first_link": data.get('links', [None])[0],  # gets the first link or None
        "first_publish_date": data.get('first_publish_date', ''),
        "book_id": book_id,
        "cover_key": cover_key 
    }

    return book_details