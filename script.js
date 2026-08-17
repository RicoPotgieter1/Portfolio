const form = document.getElementById('contact-form');

form.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(form);

    fetch('http://127.0.0.1:5000/contact', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {console.log('Form submitted successfully:', data)})
    .catch(error => {console.error('Error submitting form:', error)});
});