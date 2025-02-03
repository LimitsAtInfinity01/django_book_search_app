// utils.js

export function getData(book_info) {
    const encoded = encodeURIComponent(book_info);
    const url = `https://openlibrary.org/search.json?q=${encoded}`;

    return fetch(url).then(response => response.json());
}


// Function to get CSRF Token from cookies
export function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1] || '';
}

// Extract book data from API response
export function extractBookData(book) {
    return {
        author: book['author_name'] ? book['author_name'][0] : "Unknown",
        title: book['title'] || "Untitled",
        subtitle: book['subtitle'] || "No subtitle",
        languages: book['language'] ? book['language'].join(", ") : "N/A",
        cover_edition_key: book['cover_edition_key'],
        first_publish_year: book['first_publish_year'] || "Unknown",
        open_library_work_id: book['key']
        
    };
}

// Create text-based elements (title, author, etc.)
export function createTextElement(tag, className, textContent) {
    const element = document.createElement(tag);
    element.classList.add(className);
    element.textContent = textContent;
    return element;
}

// Create image or placeholder if no cover is available
export function createImageElement(cover_edition_key) {
    if (!cover_edition_key) {
        const span = document.createElement('span');
        span.classList.add('cover_image_not_found');
        span.textContent = 'Image not found!';
        return span;
    }

    const img = document.createElement('img');
    img.classList.add('cover_image');
    img.setAttribute('src', `https://covers.openlibrary.org/b/olid/${cover_edition_key}-M.jpg`);
    return img;
}

// Create a link element for book view
export function createBookViewLink(title, count) {
    const book_view = document.createElement('a');
    book_view.classList.add('book_view_link');
    book_view.setAttribute('href', 'view-book');
    book_view.setAttribute('id', `book_title${count}`)

    const h2_title = createTextElement('h2', 'title', title);
    book_view.appendChild(h2_title);

    return book_view;
}

// Create a form for adding books to reading list
export function createBookForm(book_data) {
    const form = document.createElement('form');
    form.setAttribute('method', 'POST');
    form.classList.add('book-form');

    // CSRF token input
    const csrfInput = document.createElement('input');
    csrfInput.setAttribute('type', 'hidden');
    csrfInput.setAttribute('name', 'csrfmiddlewaretoken');
    csrfInput.setAttribute('value', getCSRFToken());

    // Submit button
    const submit_button = document.createElement('input');
    submit_button.setAttribute('type', 'submit');
    submit_button.setAttribute('value', 'Add to Reading List');

    form.appendChild(csrfInput);
    form.appendChild(submit_button);

    // Add event listener to submit form
    form.addEventListener('submit', (event) => handleBookSubmission(event, book_data));

    return form;
}

// Handle book submission to Django backend
export function handleBookSubmission(event, book_data) {
    event.preventDefault();

    console.log(book_data)
    
    fetch('/add-to-reading-list/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify(book_data)
        
    })
    .then(response => {

        if (response.status === 302) {
            alert('You need to log in to add an item to your reading list');
            return null;
        }

        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            console.error('Response is not JSON:', response);
            return null;
        }

        return response.json();
    })
    .then(data => {
        if (!data) {
            alert('Unexpected server response');
            return;
        }

        alert(data.success ? 'Book added successfully' : `Error adding the book: ${data.message || 'Unknown error'}`);
    })
    .catch(error => console.error('Error:', error));
}

// Create and append book elements to container
export function createBookEntry(book, book_container, count) {
    const book_data = extractBookData(book);

    const bookDiv = document.createElement('div');
    bookDiv.classList.add('book');
    bookDiv.setAttribute('id', `whole_book_div${count}`)

    const book_view = createBookViewLink(book_data.title, count);
    const h3_subtitle = createTextElement('h3', 'subtitle', book_data.subtitle);
    const img = createImageElement(book_data.cover_edition_key);
    const p_author = createTextElement('p', 'author', `Author: ${book_data.author}`);
    const p_year = createTextElement('p', 'published_year', `Published Year: ${book_data.first_publish_year}`);
    const form = createBookForm(book_data);

    bookDiv.appendChild(book_view);
    bookDiv.appendChild(h3_subtitle);
    bookDiv.appendChild(img);
    bookDiv.appendChild(p_author);
    bookDiv.appendChild(p_year);
    bookDiv.appendChild(form);

    book_container.appendChild(bookDiv);
}
