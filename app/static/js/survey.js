$(document).ready(function() {
    $('#submitserveyBtn').click(function() {
        // Prevent the default action of the submit button
        event.preventDefault();

        // Get form values
        var name = $('#name').val();
        var email = $('#email').val();
        var feedback = $('#feedback').val();

        // Validate form (simple client-side validation)
        if (name === '' || email === '' || feedback === '') {
            alert('Please fill out all fields.');
            return;
        }

        // Here you can add code to send the form data to your server
        // For now, we'll just show an alert
        alert('Thank you for your feedback, ' + name + '!');

        // Close the modal
        $('#surveyModal').modal('hide');
    });
});