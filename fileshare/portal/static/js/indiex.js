// 1. Select the form by its ID
const loginForm = document.getElementById('loginForm');

// 2. Listen for the 'submit' event (not just 'click')
loginForm.addEventListener('submit', function(event) {
    
    // 3. STOP the browser from refreshing the page
    event.preventDefault(); 
    
    console.log("Form submission intercepted!");

    // 4. Perform the redirect
    // Ensure search.html is in the same folder as index.html
    window.location.href = "search.html";
});