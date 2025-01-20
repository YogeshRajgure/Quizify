document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const promptForm = document.getElementById('promptForm');

    if (uploadForm) {
        uploadForm.addEventListener('submit', function(event) {
            const fileInput = document.getElementById('fileInput');
            if (!fileInput.value) {
                event.preventDefault();
                alert('Please upload a document.');
            }
        });
    }

    if (promptForm) {
        promptForm.addEventListener('submit', function(event) {
            const promptInput = document.getElementById('promptInput');
            if (!promptInput.value) {
                event.preventDefault();
                alert('Please enter a prompt.');
            }
        });
    }
});