export class BookCard {
    constructor({ title, subtitle, imgSrc, imgAlt, authors, languages, yearPublished, cardClasses = [], cardId = "" }) {
        this.title = title;
        this.subtitle = subtitle;
        this.imgSrc = imgSrc;
        this.imgAlt = imgAlt;
        this.authors = authors;
        this.languages = languages;
        this.yearPublished = yearPublished;
        this.cardClasses = cardClasses;
        this.cardId = cardId;
    }

    createCard() {
        const card = document.createElement("div");
        card.classList.add("book-card", ...this.cardClasses);
        if (this.cardId) {
            card.id = this.cardId;
        }

        card.innerHTML = `
            <h2 class="book-title">Title: ${this.title}</h2>
            <h3 class="book-subtitle">Subtitle: ${this.subtitle}</h3>
            <div class="book-image-container">
                <img src="${this.imgSrc}" alt="${this.imgAlt}" class="book-image">
            </div>
            <p class="book-authors">Authors: ${this.authors}</p>
            <div class='language-container'>
                <p class='languages-heading'>Languages</p>
                <ul class="book-languages">
                ${this.languages.map(lang => `<li class='list-item'>${lang}</li>`).join("")}
            </ul>
            </div>

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


