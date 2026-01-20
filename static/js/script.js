// Form submission handler
document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = {
        age: document.getElementById('age').value,
        weight: document.getElementById('weight').value,
        height: document.getElementById('height').value,
        stress_level: document.getElementById('stress_level').value,
        sleep_hours: document.getElementById('sleep_hours').value,
        cycle_length: document.getElementById('cycle_length').value,
        period_length: document.getElementById('period_length').value,
        exercise_frequency: document.getElementById('exercise_frequency').value,
        diet: document.getElementById('diet').value,
        symptoms: document.getElementById('symptoms').value,
        cycle_start_date: document.getElementById('cycle_start_date').value
    };
    
    // Validate form
    if (!validateForm(formData)) {
        return;
    }
    
    // Show loading state
    const submitBtn = document.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading"></span> Processing...';
    
    try {
        // Send prediction request
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Store results in sessionStorage
            sessionStorage.setItem('predictionResults', JSON.stringify(data.result));
            
            // Redirect to results page
            window.location.href = '/results';
        } else {
            showError(data.error || 'An error occurred. Please try again.');
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to server. Please try again.');
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
});

// Form validation
function validateForm(data) {
    // Remove any existing error messages
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Check required fields
    if (!data.age || !data.weight || !data.height || !data.cycle_start_date) {
        showError('Please fill in all required fields.');
        return false;
    }
    
    // Validate age range
    if (data.age < 10 || data.age > 60) {
        showError('Age must be between 10 and 60.');
        return false;
    }
    
    // Validate weight
    if (data.weight <= 0) {
        showError('Please enter a valid weight.');
        return false;
    }
    
    // Validate height
    if (data.height <= 0) {
        showError('Please enter a valid height in meters (e.g., 1.65).');
        return false;
    }
    
    // Validate date
    const selectedDate = new Date(data.cycle_start_date);
    const today = new Date();
    if (selectedDate > today) {
        showError('Cycle start date cannot be in the future.');
        return false;
    }
    
    return true;
}

// Show error message
function showError(message) {
    const form = document.getElementById('predictionForm');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    form.insertBefore(errorDiv, form.firstChild);
    
    // Scroll to error
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Remove after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Set today's date as max for date input
document.getElementById('cycle_start_date').max = new Date().toISOString().split('T')[0];

// Format height input helper (convert feet to meters if needed)
document.getElementById('height').addEventListener('blur', function(e) {
    const value = parseFloat(e.target.value);
    if (value > 10) {
        // Likely entered in feet, convert to meters
        const meters = (value / 3.281).toFixed(2);
        if (confirm(`Did you mean ${meters} meters? Click OK to convert, Cancel to keep ${value}.`)) {
            e.target.value = meters;
        }
    }
});
