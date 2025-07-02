import requests
from requests import RequestException
from typing import Dict

# work api https://openlibrary.org/works/OL81626W.json
# book api https://openlibrary.org/search.json?q=


class BookAPI():
    def __init__(self, search_term: str, limit: int = 99) -> None:
        self.searc_term = search_term
        self.limit = f'&limit={limit}'
        self.url = f'https://openlibrary.org/search.json?q={search_term}{self.limit}'

    # docs is the list of all the works in the JSON
    def get_docs(self):
        try:
            response = requests.get(url=self.url)
            if 200 <= response.status_code <= 299:
                data = response.json()
                self.docs = data['docs']
                return self.docs
            else:
                print(response.status_code)
        except RequestException:
            return {}
    
    # get a specific doc by title
    def get_doc_by_title(self, title: str):
        self.get_docs()
        for i in range(len(self.docs)-1):
            lower_title = self.docs[i]['title'].lower()
            if lower_title == title:
                return self.docs[i]

    def get_work_id(self, doc):
        return doc['key'] 


class WorkAPI():
    def __init__(self, work_key) -> None:
        self.url = f'https://openlibrary.org/work/{work_key}.json'

    def get_work(self):
        try:
            response = requests.get(self.url)
            self.work =  response.json()
            return self.work
        except RequestException:
            return {}

    

# https://covers.openlibrary.org/b/$key/$value-$size.jpg
class CoverAPI():
    def __init__(self, value, size: str = 'M') -> None:
        self.value = value
        self.size = size

    def get_image(self):
        if self.value == 'None':
            self.url = None
        else:
            self.url = f'https://covers.openlibrary.org/b/olid/{self.value}-{self.size}.jpg?default=false'

        return self.url
