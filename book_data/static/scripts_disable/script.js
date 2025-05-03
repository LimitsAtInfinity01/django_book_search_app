// scripts.js

import { BookCard } from "./cards.js";
import { SearchOL } from "./book_search_class.js"

async function fetchBookData(search_term){
    const search = new SearchOL(search_term)
    await search.searchPromise;
    const keys = await search.returns_all_keys()
    
    const books = []
    let index = 0
    for (const key of keys){
        if (index === 10) break
        const book = await search.return_book_data(key)
        books.push(book)
        index++;
    }
    return books
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.search-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();  // Prevent page reload
        const search_box = document.querySelector('.search-box');
        const search_term = search_box.value.trim();
        if (!search_term) return; // Optionally check for empty input

        // Clear previous search results if needed
        const card_container = document.querySelector('.book_container');
        card_container.innerHTML = "";

        // Call your modified fetchBookData with the user's input
        
        try {
            const books = await fetchBookData(search_term);
            books.forEach((book, index) => {

                
                let authors = ''
                if ( book['author_name'].length > 1){
                    const sliced_names = book['author_name'].slice(0, 3)
                    sliced_names.forEach((name, index) => {
                        if ( index != sliced_names.length - 1 ){
                            authors = authors + name + ', '
                        } else {
                            authors = authors + name
                        }
                    })
                    
                } else {
                    authors = book['author_name']
                }
                
                

                // Modify the key if needed, e.g. splitting it out
                const key = book['key'].split('/')[2];
                const cover_key = book['cover_edition_key']
                console.log(book['cover_edition_key'])
                const bookData = {
                    title: book['title'],
                    imgSrc: book['cover_url'],
                    imgAlt: "book cover image",
                    authors: authors,
                    languages: book['language'],
                    yearPublished: book['first_publish_year'],
                    key: key,
                    cardClasses: ["book-card"],
                    cardId: `book${index + 1}`,
                    bookUrl: `/book_view/${key}/${cover_key}/`

                };
                
                if (book['subtitle'] !== undefined) {
                    bookData.subtitle = book['subtitle'];
                }
                const bookCard = new BookCard(bookData);
                card_container.appendChild(bookCard.createCard());
                
            });
        } catch (error) {
            console.error("Error fetching book data:", error);
        }
    });
});


