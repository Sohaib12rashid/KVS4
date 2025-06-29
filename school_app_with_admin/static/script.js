document.getElementById('studentForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        document.getElementById('message').innerText = result.message;
        this.reset();
    } catch (error) {
        document.getElementById('message').innerText = "Error saving data!";
    }
});