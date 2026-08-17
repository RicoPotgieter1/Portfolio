const form = document.getElementById('contact-form');

form.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(form);

    fetch('https://portfolio-26xe.onrender.com/contact', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {console.log('Form submitted successfully:', data)})
    .catch(error => {console.error('Error submitting form:', error)});
});