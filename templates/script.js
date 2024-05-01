const form = document.getElementById('emotion-form');
form.addEventListener('submit', async function(event) {
    event.preventDefault();
    const sentence = document.getElementById('sentence').value;

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sentence })
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const data = await response.json();
        const result = document.getElementById('result');
        result.innerHTML = `<p style="margin: 0;">Emotion: ${data.emotion}</p><p style="margin: 0;">Probability: ${data.probability}%</p>`;
        
    } catch (error) {
        console.error(error);
        result.innerHTML = "<p>Error: An error occurred during prediction.</p>";
    }
});
