// cards.js

export class BookCard {
    constructor({ title, subtitle, imgSrc, imgAlt, authors, languages, yearPublished, key, bookUrl, cardClasses = [], cardId = "" }) {
        this.title = title;
        this.subtitle = subtitle;
        this.imgSrc = imgSrc;
        this.imgAlt = imgAlt;
        this.authors = authors;
        this.languages = languages;
        this.yearPublished = yearPublished;
        this.cardClasses = cardClasses;
        this.cardId = cardId;
        this.key = key
        this.bookUrl = bookUrl;
    }

    createCard() {
        const card = document.createElement("div");
        card.classList.add("book-card", ...this.cardClasses);
        if (this.cardId) {
            card.id = this.cardId;
        }
    
        // Create title and link
        const title = document.createElement('h2');
        if(this.cardId){
            title.id = this.cardId
        }
        title.classList.add("book-title");
    
        const link = document.createElement('a');
        link.href = this.bookUrl;  // Ensure this.bookUrl exists in the class
        link.textContent = this.title; // Set text inside <a>
    
        title.appendChild(link); // Add link inside <h2>
        card.prepend(title); // Add title to the card before setting innerHTML
    
        // Append remaining content
        card.innerHTML += `
            ${this.subtitle ? `<h3 class="book-subtitle">Subtitle: ${this.subtitle}</h3>` : ""}
            <div class="book-image-container">
                <a href="${this.bookUrl}">
                    <img src="${this.imgSrc}" alt="${this.imgAlt}" class="book-image">
                </a>
            </div>
            <div class='author-container'>
                <p class='author-heading'>Authors</p>
                <p class="book-authors">${this.authors}</p>
            </div>
            <div class='language-container'>
                <p class='languages-heading'>Languages</p>
                <ul class="book-languages">
                    ${this.languages.map(lang => `<li class='list-item'>${lang}</li>`).join("")}
                </ul>
            </div>
            <span hidden class='hidden-key'>${this.key}</span>
            <p class="book-year">Year published: ${this.yearPublished}</p>
        `;
    
        return card;
    }
    

    // ✅ New method: Add a class to a selected element within the card
    addClassToElement(elementSelector, className) {
        const card = document.getElementById(this.cardId);
        if (!card) {
            console.error("Error: Card not found.");
            return;
        }

        const element = card.querySelector(elementSelector);
        if (element) {
            element.classList.add(className);
        } else {
            console.error(`Error: Element '${elementSelector}' not found in the card.`);
        }
    }
}


