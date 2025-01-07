const form = document.getElementById('upload-form');
const originalImage = document.getElementById('original-image');
const enhancedImage = document.getElementById('enhanced-image');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('image-input');
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    // Show loading state
    originalImage.src = '';
    enhancedImage.src = '';
    originalImage.alt = 'Loading...';
    enhancedImage.alt = 'Loading...';

    try {
        const response = await fetch('/enhance', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();
        if (response.ok) {
            originalImage.src = data.uploaded_image_url;
            enhancedImage.src = data.enhanced_image_url;
        } else {
            alert(data.error || 'Something went wrong!');
        }
    } catch (err) {
        console.error(err);
        alert('An error occurred. Please try again.');
    }
});
