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

// let imageedit = document.getElementById('editImageFile');

// imageedit.addEventListener('change',()=>{
//   console.log(imageedit.files[0]);
// })