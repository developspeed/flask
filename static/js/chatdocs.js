// Messaging Area

document.addEventListener('DOMContentLoaded', function () {
    const messageInput = document.getElementById('messageInput');
    const sendMessageButton = document.getElementById('sendMessageButton');
    const messagesContainer = document.getElementById('messagesContainer');

    sendMessageButton.addEventListener('click', function () {
        const message = messageInput.value.trim();
        if (message !== '') {
            appendMessage(message);
            messageInput.value = '';
        }
    });

    messageInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessageButton.click();
        }
    });

    function appendMessage(messageText) {
        const messageElement = document.createElement('div');
        messageElement.className = 'flex items-start justify-end mb-2';
        messageElement.innerHTML = `
            <div class="bg-gray-200 text-black py-2 px-4 rounded-lg max-w-md">
                ${messageText}
            </div>
        `;
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});


// Upload Files with Toast
const fileInput = document.getElementById('fileInput');
const successToast = document.getElementById('toast-success');

fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    if (files && files.length > 0) {
        console.log('Uploaded files:');
        for (const file of files) {
            console.log(file.name);
        }

        // Show the success toast
        successToast.classList.remove('hidden');

        // Hide the toast after a few seconds
        setTimeout(() => {
            successToast.classList.add('hidden');
        }, 3000);
    }
});


// After UPloading the file then show the file from user side and success message from bot side

// const fileInput = document.getElementById('fileInput'); already declared above so commented
const messagesContainer = document.getElementById('messagesContainer');

fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    if (files && files.length > 0) {
        for (const file of files) {
            const messageDivUploaded = document.createElement('div');
            messageDivUploaded.classList.add('flex', 'items-start', 'mb-2','justify-end');
            messageDivUploaded.innerHTML = `
                <div class="bg-green-100 text-black py-2 px-4 rounded-lg max-w-md">
                Uploaded Files :  
                    ${file.name}
                </div>`;
            messagesContainer.appendChild(messageDivUploaded);

            const messageDivUploadedSuccess = document.createElement('div');
            messageDivUploadedSuccess.classList.add('flex', 'items-start', 'mb-2');
            messageDivUploadedSuccess.innerHTML = `
                <div class="bg-blue-500 text-white py-2 px-4 rounded-lg max-w-md">
                Please wait while we are scanning the file contents :)
                </div>`;
            messagesContainer.appendChild(messageDivUploadedSuccess);

        }

        // Show the success toast
        const successToast = document.getElementById('toast-success');
        successToast.classList.remove('hidden');

        // Hide the toast after a few seconds
        setTimeout(() => {
            successToast.classList.add('hidden');
        }, 3000);
    }
});


// Sending the uploaded file the the server

// const fileInput = document.getElementById('fileInput'); already declared 
const sendMessageButton = document.getElementById('sendMessageButton');
const messageInput = document.getElementById('messageInput');
fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    if (files && files.length > 0) {
        // Create a FormData object to hold the files
        const formData = new FormData();
        for (const file of files) {
            formData.append('files', file);
        }

        // Send files to the server using AJAX
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Files uploaded:', data);
        })
        .catch(error => {
            console.error('Error uploading files:', error);
        });
    }
});

sendMessageButton.addEventListener('click', () => {
    const message = messageInput.value;
    // Send the message to the server using AJAX
    // Your AJAX code here...
});