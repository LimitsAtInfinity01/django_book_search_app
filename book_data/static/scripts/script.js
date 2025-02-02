
const submit_button = document.querySelector('.submit-search')
const book_container = document.querySelector('.book_container')

submit_button.addEventListener('click', event => {
    event.preventDefault();
    const search_term = document.querySelector('.search-box').value;
    book_container.innerHTML = ''
    getData(search_term)
})

function getCSRFToken() {
    let csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return csrfToken;
}

function getData(book_info) {

    const encoded = encodeURIComponent(book_info)
    const url = `https://openlibrary.org/search.json?q=${encoded}`

    return fetch(url)
    .then(responce => responce.json())
    .then(data => {

        const book_container = document.querySelector('.book_container')

        data.docs.forEach((book, index) => {

            if (index >= 3) return;

            const author = book['author_name'] ? book['author_name'][0] : "Unknown";
            const title = book['title'] || "Untitled";
            const subtitle = book['subtitle']  || "No subtitle"
            const languages = book['language'] ? book['language'].join(", ") : "N/A";
            const cover_edition_key = book['cover_edition_key'];
            const first_publish_year = book['first_publish_year'] || "Unknown";
            const open_library_work_id = book['key'] 
            console.log(open_library_work_id)
            // Create an object witht the book data to send it Django through the form
            const book_data = {
                author: author,
                title: title,
                open_library_work_id: open_library_work_id,
                subtitle: subtitle,
                languages: languages,
                cover_edition_key: cover_edition_key,
                first_publish_year: first_publish_year
            }
            

            const image_url = `https://covers.openlibrary.org/b/olid/${cover_edition_key}-M.jpg`

            const bookDiv = document.createElement('div');
            bookDiv.classList.add('book');
            
            const h2_title = document.createElement('h2');
            h2_title.classList.add('title');
            book_container.appendChild(h2_title);

            const h3_subtitle = document.createElement('h3');
            h3_subtitle.classList.add('subtitle');
            book_container.appendChild(h3_subtitle);

            const p_author = document.createElement('p');
            p_author.classList.add('author');
            book_container.appendChild(p_author);
            
            const p_year = document.createElement('p');
            p_year.classList.add('published_year');
            book_container.appendChild(p_year);

            let img = null;
            if (cover_edition_key === undefined){
                img = document.createElement('span')
                img.classList.add('cover_image_not_found')
                book_container.appendChild(img)

            } else {
                img = document.createElement('img')
                img.classList.add('cover_image')
                book_container.appendChild(img)
            }

            // Create form with CSRF token
            const form = document.createElement('form');
            form.setAttribute('method', 'POST');
            form.classList.add('book-form');

            // Create CSRF token input
            const csrfInput = document.createElement('input');
            csrfInput.setAttribute('type', 'hidden');
            csrfInput.setAttribute('name', 'csrfmiddlewaretoken');
            csrfInput.setAttribute('value', getCSRFToken()); // Set token from cookie

            // Append CSRF token to form
            form.appendChild(csrfInput);

            // Create submit button
            const submit_button = document.createElement('input');
            submit_button.setAttribute('type', 'submit');
            submit_button.setAttribute('value', 'Add to Reading List');

            form.appendChild(submit_button);

            // Append elements to book div
            bookDiv.appendChild(h2_title);
            bookDiv.appendChild(h3_subtitle)
            bookDiv.append(img)
            bookDiv.appendChild(p_author);
            bookDiv.appendChild(p_year);
            bookDiv.append(form)
            

            h2_title.textContent = title;
            h3_subtitle.textContent = subtitle;
            p_author.textContent = `Author: ${author}`;
            p_year.textContent = `Published Year: ${first_publish_year}`;

            if (cover_edition_key !== undefined) {
                img.setAttribute('src', image_url);
            } else {
                img.textContent = 'Image not found!';
            }

            // Append book div to the main container
            book_container.appendChild(bookDiv);

            form.addEventListener('click', (event) => {
                event.preventDefault();
                console.log('Button Pressed')

                fetch('/add-to-reading-list/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify(book_data)
                })
                .then(response => response.json())
                .then(data => {
                    if(data.success){
                        alert('Book added sucessfully')
                    } else {
                        alert('Error adding the book')
                    }
                })
                .catch(error => console.error('Error', error));
            })

        });
    })
}
// stephen king

// console.log(`Book ${index + 1}:`);
// console.log(`Title: ${title}`);
// console.log(`Author: ${author}`);
// console.log(`Languages: ${languages}`);
// console.log(`First Published: ${first_publish_year}`);
// console.log(`Cover Key: ${cover_edition_key}`);
// console.log("------------------------------------------------");

