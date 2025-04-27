/**
 * Direct handler for Django admin to update performer dropdown when event changes
 */
(function() {
    // Run this code immediately
    console.log('Direct select handler starting');
    
    // Try to set up event handlers immediately and then again after DOM is loaded
    setupEventHandlers();
    
    // Also run when the DOM is fully loaded
    document.addEventListener('DOMContentLoaded', function() {
        console.log('DOM loaded, setting up event handlers');
        setupEventHandlers();
        
        // Try again after a short delay to catch any late initialization
        setTimeout(setupEventHandlers, 500);
        setTimeout(setupEventHandlers, 1000);
    });
    
    // Function to set up the event handlers
    function setupEventHandlers() {
        // Find the event and performer select elements
        var eventSelect = document.getElementById('id_event');
        var performerSelect = document.getElementById('id_performer');
        
        if (!eventSelect || !performerSelect) {
            console.log('Event or performer select not found, will try again later');
            return;
        }
        
        console.log('Found both select elements, setting up handler');
        
        // Function to update performers based on selected event
        function updatePerformers() {
            var eventId = eventSelect.value;
            console.log('Event changed to:', eventId);
            
            if (!eventId) {
                // Clear performer options if no event selected
                performerSelect.innerHTML = '<option value="">---------</option>';
                return;
            }
            
            // Show loading indicator
            performerSelect.innerHTML = '<option>Loading performers...</option>';
            
            // Fetch performers for the selected event
            fetch('/api/get_event_performers/?event_id=' + eventId + '&_=' + new Date().getTime())
                .then(function(response) {
                    if (!response.ok) {
                        throw new Error('Network response was not ok: ' + response.status);
                    }
                    return response.json();
                })
                .then(function(data) {
                    console.log('Received performers:', data);
                    
                    // Clear existing options
                    performerSelect.innerHTML = '';
                    
                    // Add empty option
                    var emptyOption = document.createElement('option');
                    emptyOption.value = '';
                    emptyOption.textContent = '---------';
                    performerSelect.appendChild(emptyOption);
                    
                    // Add performers from the response
                    if (data.length === 0) {
                        var noPerformersOption = document.createElement('option');
                        noPerformersOption.disabled = true;
                        noPerformersOption.textContent = 'No performers for this event';
                        performerSelect.appendChild(noPerformersOption);
                    } else {
                        data.forEach(function(performer) {
                            var option = document.createElement('option');
                            option.value = performer.id;
                            option.textContent = performer.name;
                            performerSelect.appendChild(option);
                        });
                        console.log('Added ' + data.length + ' performers to dropdown');
                    }
                })
                .catch(function(error) {
                    console.error('Error fetching performers:', error);
                    performerSelect.innerHTML = '<option value="">Error loading performers</option>';
                });
        }
        
        // Remove any existing event listeners (to avoid duplicates)
        eventSelect.removeEventListener('change', updatePerformers);
        
        // Add change event listener to event select
        eventSelect.addEventListener('change', updatePerformers);
        console.log('Added change event listener to event select');
        
        // Also intercept the Django admin's select box enhancements
        if (typeof django !== 'undefined' && django.jQuery) {
            django.jQuery(eventSelect).off('change.performers').on('change.performers', function() {
                console.log('jQuery change event detected');
                updatePerformers();
            });
        }
        
        // Run immediately if an event is already selected
        if (eventSelect.value) {
            console.log('Event already selected (' + eventSelect.value + '), updating performers');
            updatePerformers();
        }
    }
})(); 