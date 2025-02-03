import { getData, createBookEntry, getCSRFToken } from './get_book_data.js';

const submit_button = document.querySelector('.submit-search');
const book_container = document.querySelector('.book_container');


const books = [];
const title_links = [];
const book_divs = []

function individualBookView() {
    if (title_links.length > 0) {

        title_links.forEach((link, index) => link.addEventListener('click', event => {
            
            const title_from_books =  books[index].title
            const title_from_element = book_divs[index].querySelector('.title').textContent

            let subtitle_from_books = books[index].subtitle
            const subtitle_from_element = book_divs[index].querySelector('.subtitle').textContent
            if (subtitle_from_books === undefined){
                subtitle_from_books = 'No subtitle'
            }

            if (title_from_element === title_from_books
                && subtitle_from_books === subtitle_from_element)
            {

                fetch('/view-book', {  // ✅ Ensure this matches `urls.py`
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify(books[index])
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Server response:', data);
                    if (!data) {
                        alert('Unexpected server response');
                    }
                })
                .catch(error => console.error('Error:', error));
            }

        }))

    }
}




submit_button.addEventListener('click', event => {
    event.preventDefault();
    const search_term = document.querySelector('.search-box').value;
    book_container.innerHTML = ''; 
    books.length = 0;
    title_links.length = 0;

    getData(search_term).then(data => {
        data.docs.slice(0, 3).forEach((book, index) => {
            books.push(book);
            createBookEntry(book, book_container, index);
            let linkElement = document.getElementById(`book_title${index}`);
            if (linkElement) {
                title_links.push(linkElement);
            }

            let bookDiv = document.getElementById(`whole_book_div${index}`)
            if(bookDiv){
                book_divs.push(bookDiv)
            }

        });

        // Call function that processes title_links
        individualBookView();
    });
});


// {'author_key': ['OL33088A', 'OL36575A'], 
// 'author_name': ['Dean Koontz', 'Kevin J. Anderson'], 
// 'cover_edition_key': 'OL24943649M', 
// 'cover_i': 6956759, 
// 'edition_count': 21, 
// 'first_publish_year': 2005, 
// 'has_fulltext': True, 
// 'public_scan_b': False, 
// 'subtitle': 'Prodigal Son', 
// 'title': "Dean Koontz's Frankenstein"}