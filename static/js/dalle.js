// Taking input from the mic using webspeech recognition api

const micIcon = document.getElementById("change1");
let isRecording = false;
let recognition;
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





const micIcon2 = document.getElementById("change2");
let isRecording2 = false;
let recognition2;
micIcon2.addEventListener("click", toggleRecording2);

function toggleRecording2() {
  if (isRecording2) {
    stopRecording2();
  } else {
    startRecording2();
  }
  isRecording2 = !isRecording2;
}

function startRecording2() {
  micIcon2.style.color = 'red';
  recognition2 = new window.webkitSpeechRecognition() || new window.SpeechRecognition();
//   recognition.lang = "en-US"; // Set the language for speech recognition
  recognition2.continuous = true;
  
  recognition2.onstart = function () {
    // console.log("Recording started");
  };

  recognition2.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    let text = document.getElementById('prompt2');
    // console.log("Transcript:", transcript);
    text.value = transcript;
    stopRecording2()
    // micIcon.click()
    // Handle the recognized speech transcript here
  };

  recognition2.start();
}

function stopRecording2() {
  micIcon2.style.color = "gray";
  recognition2.stop();
  // console.log("Recording stopped");
}
