// Load and display results
window.addEventListener('DOMContentLoaded', function() {
    // Get results from sessionStorage
    const resultsJSON = sessionStorage.getItem('predictionResults');
    
    if (!resultsJSON) {
        // No results found, redirect back to form
        window.location.href = '/';
        return;
    }
    
    try {
        const results = JSON.parse(resultsJSON);
        
        // Display BMI
        document.getElementById('bmi-value').textContent = results.bmi || '--';
        
        // Display next cycle date
        const nextCycleDate = results.predicted_next_cycle_start_date;
        if (nextCycleDate) {
            // Format date nicely
            const date = new Date(nextCycleDate);
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            const formattedDate = date.toLocaleDateString('en-US', options);
            document.getElementById('next-cycle').textContent = formattedDate;
        } else {
            document.getElementById('next-cycle').textContent = '--';
        }
        
        // Display accuracy
        document.getElementById('accuracy').textContent = results.accuracy || '--';
        
        // Add animation
        animateResults();
        
    } catch (error) {
        console.error('Error parsing results:', error);
        window.location.href = '/';
    }
});

// Animate results display
function animateResults() {
    const resultValues = document.querySelectorAll('.result-value');
    resultValues.forEach((element, index) => {
        setTimeout(() => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            element.style.transition = 'all 0.5s ease';
            
            setTimeout(() => {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, 50);
        }, index * 150);
    });
}

// Go back to form
function goBack() {
    // Clear results
    sessionStorage.removeItem('predictionResults');
    window.location.href = '/';
}

// Add keyboard shortcut to go back (Escape key)
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        goBack();
    }
});
