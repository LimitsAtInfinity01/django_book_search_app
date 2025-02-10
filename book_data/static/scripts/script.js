import { BookCard } from "./cards.js";
import { SearchOL } from "./book_search_class.js"

async function fetchBookData(){
    const search = new SearchOL('stephen king')
    await search.searchPromise;
    const keys = search.returns_all_keys()
    const key = await search.return_book_key_by_title('carrie')
    const book_metadata = await search.return_book_data(key)
    return book_metadata
}

document.addEventListener('DOMContentLoaded', ()=> {
    
    const book_metadata = fetchBookData()
    book_metadata.then(data => {

    const card_container = document.querySelector('.book_container')

    const bookCard = new BookCard({
        title: data['title'],
        subtitle: 'Subtitle Here',
        imgSrc: data['cover_url'],
        imgAlt: "book cover image",
        authors: data['author_name'],
        languages: data['language'],
        yearPublished: data['first_publish_year'],

        cardClasses: ["book-card", "shadow"],
        cardId: "book1"
    });

    card_container.appendChild(bookCard.createCard())

    })
})

