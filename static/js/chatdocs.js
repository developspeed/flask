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

        // // Show the success toast
        // successToast.classList.remove('hidden');

        // // Hide the toast after a few seconds
        // setTimeout(() => {
        //     successToast.classList.add('hidden');
        // }, 3000);
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
            messageDivUploaded.classList.add('flex', 'items-start', 'mb-2', 'justify-end');
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
    }
});


// Sending the uploaded file the the server

// const fileInput = document.getElementById('fileInput'); already declared 

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
                // Show the success toast
                const successToast = document.getElementById('toast-success');
                const successMessage = document.getElementById('success-message')
                successToast.classList.remove('hidden');
                successMessage.innerHTML = data.message; //Server returns a response after uploading the file successfully 

                // Hide the toast after a few seconds
                setTimeout(() => {
                    successToast.classList.add('hidden');
                }, 3000);
                console.log('Files uploaded:', data);
            })
            .catch(error => {
                const errorToast = document.getElementById('toast-error');
                const errorMessage = document.getElementById('error-message')
                errorToast.classList.remove('hidden');
                errorMessage.innerText = 'An error occurred during upload';

                setTimeout(() => {
                    errorToast.classList.add('hidden');
                }, 3000);
                console.error('Error uploading files:', error);
            });
    }
});

const sendMessageButton = document.getElementById('sendMessageButton');
const messageInput = document.getElementById('messageInput');
// const messagesContainer = document.getElementById('messagesContainer');  Already declared

sendMessageButton.addEventListener('click', () => {
    const userMessage = messageInput.value;

    if (userMessage.trim() !== '') {
        messageInput.value = ''; // Clear input field

        // Append user message to messages container
        appendMessage(userMessage, true);

        // Display waiting message
        const waitingMessageDiv = document.createElement('div');
        waitingMessageDiv.classList.add('flex', 'items-start', 'mb-2');
        waitingMessageDiv.innerHTML = `
            <div class="bg-blue-200 text-black py-2 px-4 rounded-lg max-w-md">
                Waiting for response...
            </div>`;
        messagesContainer.appendChild(waitingMessageDiv);

        // Send message to the server
        let formData = new FormData();
        formData.append('userMessage', userMessage);
        fetch('/chatdocs', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Remove waiting message
            messagesContainer.removeChild(waitingMessageDiv);

            // Display server response
            const responseMessageDiv = document.createElement('div');
            responseMessageDiv.classList.add('flex', 'items-start', 'mb-2');
            responseMessageDiv.innerHTML = `
                <div class="bg-green-500 text-white py-2 px-4 rounded-lg max-w-md">
                    ${data.response}
                </div>`;
            messagesContainer.appendChild(responseMessageDiv);
        })
        .catch(error => {
            console.error('Error sending/receiving messages:', error);
            // Remove waiting message
            messagesContainer.removeChild(waitingMessageDiv);

            // Display error message
            const errorMessageDiv = document.createElement('div');
            errorMessageDiv.classList.add('flex', 'items-start', 'mb-2');
            errorMessageDiv.innerHTML = `
                <div class="bg-red-500 text-white py-2 px-4 rounded-lg max-w-md">
                    An error occurred: ${error.message}
                </div>`;
            messagesContainer.appendChild(errorMessageDiv);
        });
    }
});

function appendMessage(message, isUserMessage = false) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('flex', 'mb-2', 'justify-' + (isUserMessage ? 'end' : 'start'));
    
    const messageContent = document.createElement('div');
    messageContent.classList.add('py-2', 'px-4', 'rounded-lg', 'max-w-md');
    
    if (isUserMessage) {
        messageContent.classList.add('bg-gray-200', 'text-gray-900');
    } else {
        messageContent.classList.add('bg-gray-200', 'text-black');
    }

    messageContent.textContent = message;
    messageElement.appendChild(messageContent);

    messagesContainer.appendChild(messageElement);
}
