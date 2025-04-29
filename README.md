# Bookish

## A Powerful Tool for Finding Your Next Read  

### Introduction  
Bookih is a user-friendly application designed to help readers discover books based on their preferences. Whether you're searching for a specific title, author, or genre, this tool provides a seamless experience for book enthusiasts.

This is a perfect application if you want to create private social medias for book clubs or book lovers. It's features such as following other readers, book reviews, comments, and profile pages makes it so you can interect with many readers and share your thought about many books.

#### Features
- Search for book information.
- Create an account with a username and password.
- Write reviews of your favorite books.
- Make favorite and reading lists.
- Comment in others' reviews.
- Create profile pages.


### Techmical Description
This web application is written in python using the Django framework, HTML, CSS and JavaScript. It request metadata from the Open Library API `https://openlibrary.org/developers/api` about books, and other written records. Then dynamically process that data when the user makes searches and displays the results in a readable, friendly manner. 


## Demo Video

<div align="center">

  [![Watch the video](https://img.youtube.com/vi/zD6feUQRxkc/0.jpg)](https://youtu.be/zD6feUQRxkc)

</div>


### Installation and Usage Instructions (For End-Users)  
1. **Installation**:  
    - Clone the repository:  
      ```bash  
      git clone https://github.com/yourusername/book_search.git  
      ```  
    - Navigate to the project directory:  
      ```bash  
      cd book_search  
      ```  
    - Install dependencies:  
      ```bash  
      python3 -m venv venv
      source venv/bin/activate    # (Linux/macOS)

      or

      venv\Scripts\activate       # (Windows)

      ```  
    - Start the application:  
      ```bash  
      python manage.py runserver 
      ```  

2. **Usage**:  
    - Open your browser and navigate to `http://localhost:3000`.  
    - Use the search bar to find books by title, author, or genre.  

### Installation and Usage Instructions (For Contributors)  
1. **Setup for Development**:  
    - Fork the repository and clone it locally.  
    - Install dependencies using `pip install -r requirements.txt`.  
    - Run the development server with `python manage.py runserver`.  

2. **Development Guidelines**:  
    - Ensure all code changes are tested.  
    - Follow the existing code style and structure.  

### Contributor Expectations  
- Create an issue before submitting a pull request.  
- Use descriptive commit messages.  


### Known Issues  
- This is a work in progress. There are many features that need finishing. 
- Homepage needs a more descriptive summary of the application.
- Favorite books page is incomplete.
- Need better, more attractive CSS style for profile pages.
- Some refractoring and OOP approach for the Django views in `views.py`. 
- Needs performance optimization when accessing reading list pages.
- etc. 
