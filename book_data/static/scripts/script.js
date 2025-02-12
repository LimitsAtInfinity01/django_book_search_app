// scripts.js

import { BookCard } from "./cards.js";
import { SearchOL } from "./book_search_class.js"

async function fetchBookData(){
    const search = new SearchOL('stephen king')
    await search.searchPromise;
    const keys = await search.returns_all_keys()
    
    const books = []
    let index = 0
    for (const key of keys){
        if (index === 3) break
        const book = await search.return_book_data(key)
        books.push(book)
        index++;
    }
    return books
}

document.addEventListener('DOMContentLoaded', ()=> {
    
    const books = fetchBookData()
    books.then(data => {
    
    data.forEach((book, index) => {
        const card_container = document.querySelector('.book_container')
        console.log(book['key'].split('/')[2])
        const key = book['key'].split('/')[2]
        const bookData = {
            title: book['title'],
            imgSrc: book['cover_url'],
            imgAlt: "book cover image",
            authors: book['author_name'],
            languages: book['language'],
            yearPublished: book['first_publish_year'],
            key: key,
            cardClasses: ["book-card"],
            cardId: `book${index+1}`,
            bookUrl: `/book/${key}`
        }

        if (book['subtitle'] != undefined){
            bookData.subtitle = book['subtitle']
        }
        const bookCard = new BookCard(bookData);
        card_container.appendChild(bookCard.createCard())
        })
    })


})

