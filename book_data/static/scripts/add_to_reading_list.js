function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1] || '';
}

function addToReadingList(book_info){
    fetch('add-to-reading-list/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken() // Include CSRF token
        },
        body: JSON.stringify(book_info)
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            alert('Book added successfully')
        } else {
            alert('Error ' + (data.message || 'Unknown error'));
        }
    })
}

document.addEventListener('DOMContentLoaded', () => {
    const addButton = document.getElementById('add-to-reading-list')


    if(addButton){
        addButton.addEventListener('click', event => {

            fetch('get-book-info/')
            .then(response => response.json())
            .then(data => {
                if(data.success){
                    console.log(data)
                    addToReadingList(data.book_info)

                } else {
                    alert('No book data available')
                }
            })

        })
    }

})

// 'open_library_work_id': '/works/OL263273W'