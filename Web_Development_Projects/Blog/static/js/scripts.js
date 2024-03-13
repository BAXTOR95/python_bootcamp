/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
})

document.addEventListener("DOMContentLoaded", function() {
    const submitButton = document.getElementById('submitButton');
    const form = document.getElementById('contactForm');
    const name = document.getElementById('name');
    const email = document.getElementById('email');
    const phone = document.getElementById('phone');
    const message = document.getElementById('message');

    // Initially disable the submit button
    submitButton.disabled = true;

    // Function to check the validity of the form
    function validateForm() {
        // Check each input field to see if it's valid
        const isValid = name.value.trim() !== '' && email.value.trim() !== '' && phone.value.trim() !== '' && message.value.trim() !== '' && email.checkValidity();

        // Enable or disable the submit button based on the form validity
        submitButton.disabled = !isValid;
    }

    // Attach event listeners to input fields to validate the form on input
    [name, email, phone, message].forEach(input => {
        input.addEventListener('input', validateForm);
    });
});

window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function() {
        $(this).remove();
    });
}, 5000);