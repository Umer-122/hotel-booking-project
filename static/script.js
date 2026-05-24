document.getElementById('bookingForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    try {
        const response = await fetch('/book', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            alert(data.message);
            this.reset();
        } else {
            alert('Error: ' + data.detail);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});