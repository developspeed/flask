// Taking input from the mic using webspeech recognition api

const micIcon = document.getElementById("change");
let isRecording = false;
let recognition;
// console.log('loaded')
micIcon.addEventListener("click", toggleRecording);

function toggleRecording() {
  if (isRecording) {
    stopRecording();
  } else {
    startRecording();
  }
  isRecording = !isRecording;
}

function startRecording() {
  micIcon.style.color = 'red';
  recognition = new window.webkitSpeechRecognition() || new window.SpeechRecognition();
//   recognition.lang = "en-US"; // Set the language for speech recognition
  recognition.continuous = true;
  
  recognition.onstart = function () {
    // console.log("Recording started");
  };

  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    let text = document.getElementById('prompt');
    // console.log("Transcript:", transcript);
    text.value = transcript;
    stopRecording()
    // micIcon.click()
    // Handle the recognized speech transcript here
  };

  recognition.start();
}

function stopRecording() {
  micIcon.style.color = "gray";
  recognition.stop();
  // console.log("Recording stopped");
}

// Sending the form data params to the backend server

// let formData = new FormData();

// let prompts = document.getElementById('prompt');
// let numImages = document.getElementById('numImages');
// let sizes = document.getElementById('sizes');
// let submit = document.getElementById('submit');



// submit.addEventListener('click',()=>{
//     formData.append('prompts',prompts.value);
//     formData.append('numImages',numImages.value);
//     formData.append('sizes',sizes.value);

//     fetch('/dalle-results',{
//         method: "POST",
//         body: formData,
//     })
//     .then((response) => {
//         const data = response.json()
//         console.log(response.images);
//       })
//       .catch((error) => {
//         console.error(error);
//       });
// });