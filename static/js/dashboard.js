let fileUploader = document.getElementById('uploadFiles');

fileUploader.addEventListener('change', () => {
    // alert('Uploading...')
    let filesToUpload = fileUploader.files[0];
    let formData = new FormData();
    let uploadedFileCopy = document.getElementById('uploadedFileCopy');
    formData.append('userFiles', filesToUpload);
    fetch('/userFilesUpload', {
        method: 'POST',
        body: formData
    })
        .then((response) => response.text())
        .then((response) => {
            console.log(response);
            alert('Uploaded!')

            // Create a temporary input element
            uploadedFileCopy.addEventListener('click', () => {
                let input = document.createElement("input");
                input.value = response;
                document.body.appendChild(input);

                // Select the text inside the input element
                input.select();
                input.setSelectionRange(0, 9999999);

                // Copy the text to the clipboard
                document.execCommand("copy");

                // Remove the temporary input element
                document.body.removeChild(input);
                uploadedFileCopy.innerHTML = 'Copied!'
                // Provide user feedback
                alert("Link copied to clipboard");
            })
        });
})