jQuery(document).ready(function($) {
    // Check if event handler is already attached
    var isEventHandlerAttached = false;

    // Function to open popup
    var openPopup = function(event) {
        event.preventDefault();
        $('.cd-popup').addClass('is-visible');
    };

    // Function to close popup
    var closePopup = function(event) {
        if ($(event.target).is('.cd-popup-close') || $(event.target).is('.cd-popup')) {
            event.preventDefault();
            $('.cd-popup').removeClass('is-visible');
        }
    };

    // Attach event handlers only if not already attached
    if (!isEventHandlerAttached) {
        // Open popup on click
        $('.cd-popup-trigger').on('click', openPopup);

        // Close popup when clicking outside or pressing 'Esc' key
        $(document).on('click keyup', closePopup);

        // Set the flag to indicate that event handlers are attached
        isEventHandlerAttached = true;
    }
});
