(function($) {
    $(document).ready(function() {
        console.log('Admin Performance Form Script Loaded');
        
        // Wait a very short time to ensure DOM is fully ready
        setTimeout(function() {
            // Get the event and performer select elements
            var eventSelect = $('#id_event');
            var performerSelect = $('#id_performer');
            
            console.log('Event select found:', eventSelect.length > 0);
            console.log('Performer select found:', performerSelect.length > 0);
            
            if (!eventSelect.length || !performerSelect.length) {
                console.error('Could not find the event or performer select elements!');
                return;
            }
            
            // Function to update performer options based on selected event
            function updatePerformerOptions() {
                var eventId = eventSelect.val();
                console.log('Event selected:', eventId);
                
                if (!eventId) {
                    console.log('No event selected, clearing performer options');
                    performerSelect.empty().append($('<option></option>').val('').text('---------'));
                    return;
                }
                
                // Show loading indicator
                performerSelect.empty().append($('<option></option>').text('Loading performers...'));
                
                // Make AJAX request to get performers for this event
                $.ajax({
                    url: '/api/get_event_performers/',
                    data: { 'event_id': eventId },
                    dataType: 'json',
                    success: function(data) {
                        console.log('AJAX success, received data:', data);
                        
                        var selectedPerformer = performerSelect.val();
                        performerSelect.empty();
                        
                        // Add empty option
                        performerSelect.append($('<option></option>').val('').text('---------'));
                        
                        if (data.length === 0) {
                            console.log('No performers found for this event');
                            performerSelect.append($('<option></option>').attr('disabled', true).text('No performers are associated with this event'));
                        } else {
                            console.log('Adding ' + data.length + ' performers to dropdown');
                            
                            // Add performers from the response
                            $.each(data, function(index, performer) {
                                var option = $('<option></option>').val(performer.id).text(performer.name);
                                if (performer.id == selectedPerformer) {
                                    option.attr('selected', 'selected');
                                }
                                performerSelect.append(option);
                            });
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error('AJAX Error:', status, error);
                        console.error('Response:', xhr.responseText);
                        
                        performerSelect.empty()
                            .append($('<option></option>').val('').text('---------'))
                            .append($('<option></option>').attr('disabled', true).text('Error loading performers'));
                    }
                });
            }
            
            // Important: Unbind any existing event handlers first to avoid duplicates
            eventSelect.off('change.performerUpdate');
            
            // Add change event handler with a namespace to avoid conflicts
            eventSelect.on('change.performerUpdate', function() {
                console.log('Event change detected');
                updatePerformerOptions();
            });
            
            // Trigger update immediately if event is already selected
            if (eventSelect.val()) {
                console.log('Event already selected on page load, updating performers');
                updatePerformerOptions();
            }
            
            // If the performer dropdown already has values (like after validation error), 
            // don't overwrite them
            if (performerSelect.find('option').length <= 1 && eventSelect.val()) {
                console.log('Performer dropdown is empty but event is selected, loading performers');
                updatePerformerOptions();
            }
            
            // For debugging purposes, show an alert so we know this script is running
            console.log('Script initialization complete');
        }, 100);  // Small delay to ensure DOM is ready
    });
})(django.jQuery); 