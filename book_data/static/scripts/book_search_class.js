// book_search_class.js

export class SearchOL {
    constructor(search_term) {
        this.search_term = encodeURIComponent(search_term);
        this.open_library_api_url = `https://openlibrary.org/search.json?q=${this.search_term}`;
        this.cover_id = null;
        this.complete_cover_url = null;

        // Automatically fetch general search results when object is created
        this.searchPromise = this.general_search();
    }

    async general_search() {
        try {
            const response = await fetch(this.open_library_api_url);
            if (!response.ok) throw new Error("Failed to fetch search results");
            const data = await response.json();
            this.general_search_results = data.docs || []; // Ensure `docs` is always an array
        } catch (error) {
            console.error("Error fetching search results:", error);
            this.general_search_results = []; // Fallback to empty array
        }
    }

    

    async ensureSearchReady() {
        await this.searchPromise;
        if (!this.general_search_results.length) throw new Error("No search results available");
    }

    async cover_url(cover_id) {
        if (!cover_id) {
            return "https://via.placeholder.com/150?text=No+Cover";
        }
        this.cover_id = cover_id;
        this.complete_cover_url = `https://covers.openlibrary.org/b/olid/${this.cover_id}-M.jpg`;
    
        try {
            const response = await fetch(this.complete_cover_url);
            return response.ok ? this.complete_cover_url : "https://via.placeholder.com/150?text=No+Cover";
        } catch (error) {
            console.error("Error fetching cover image:", error);
            return "https://via.placeholder.com/150?text=Error";
        }
    }
    

    async search_title(title) {
        await this.ensureSearchReady();
        const result = this.general_search_results.find(
            book => book.title?.toLowerCase() === title.toLowerCase()
        );
        return result ? result.title : "Title not found";
    }

    async book_key_by_title(title) {
        await this.ensureSearchReady();
        const result = this.general_search_results.find(
            book => book.title?.toLowerCase() === title.toLowerCase()
        );
        return result ? result.key : "Book key not found";
    }

    async returns_all_keys(){
        const keys = []
        const results = this.general_search_results
        results.map(result => keys.push(result['key']))
        return keys
    }

    async return_book_data(book_key) {
        await this.ensureSearchReady();
        const result = this.general_search_results.find(book => book.key === book_key);
        
        if (!result) return "Book data not found";
    
        return {
            author_key: result.author_key || [],
            author_name: result.author_name || ["Unknown Author"],
            cover_edition_key: result.cover_edition_key || null,
            cover_url: result.cover_edition_key 
                ? await this.cover_url(result.cover_edition_key) 
                : "/static/images/books.jpeg",
            first_publish_year: result.first_publish_year || "Unknown Year",
            key: book_key,
            language: result.language || ["Unknown Language"],
            title: result.title || "Unknown Title",
            subtitle: result.subtitle || "",
        };
    }
    
}


