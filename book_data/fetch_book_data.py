import requests
from book_data.lo_api_wrapper.wrapper import BookAPI, WorkAPI, CoverAPI


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
    pass

