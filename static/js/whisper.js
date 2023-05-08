// Voice Recorder with Duration to Server

let startButton = document.getElementById("startButton");
let stopButton = document.getElementById("stopButton");
let mediaRecorder;
let chunks = [];

function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();
    startButton.disabled = true;
    stopButton.disabled = false;

    mediaRecorder.ondataavailable = function (e) {
      chunks.push(e.data);
    };

    mediaRecorder.onstop = function (e) {
      let audioBlob = new Blob(chunks, { type: "audio/mp3; codecs=opus" });
      let audioUrl = URL.createObjectURL(audioBlob);
      const audioPlayer = document.getElementById("audio-player");
      const audioElement = new Audio(audioUrl);
      audioPlayer.src = audioUrl;
      let formData = new FormData();
      

      //   Duration Getting

      const audioContext = new AudioContext();
      const fileReader = new FileReader();
      var minutes = 0;
       
      fileReader.onload = function () {
        let audioFile = new File([fileReader.result], "recording.wav", {type: "audio/wav",});
        formData.append("audio", audioFile);
        audioContext
          .decodeAudioData(fileReader.result)
          .then(function (decodedData) {
            const duration = decodedData.duration;
            minutes = duration / 60;
            // var data = { duration: minutes };
            formData.append("duration", minutes);
            console.log(minutes);
            fetch("/upload", {
              method: "POST",
              body: formData,
            })
              .then(function (response) {
                console.log("Audio file uploaded successfully!");
              })
              .catch(function (error) {
                console.error("Error uploading audio file:", error);
              });
          });
      };

      // audio duration send to server

      fileReader.readAsArrayBuffer(audioBlob);
    };
  });
}

function stopRecording() {
  mediaRecorder.stop();
  startButton.disabled = false;
  stopButton.disabled = true;
  mediaRecorder.stream.getTracks().forEach(track => track.stop());
}

startButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

// Audio Player for uploaded audio and duration to server
const audioFile = document.getElementById("audioFile");
const audioFilePlayer = document.getElementById("audio-upload-player");
const uploader = document.getElementById('upload-message');
audioFile.addEventListener("change", function () {
  const file = audioFile.files[0];
  uploader.style.display = 'flex';
  uploader.style.color = 'blue';
  // console.log(file)
  let formData = new FormData();
  formData.append("audio", file);
  audioFilePlayer.addEventListener("loadedmetadata", function () {
    var duration = audioFilePlayer.duration;
    var minutes = duration / 60;
    // var seconds = duration % 60;
    console.log(minutes);
    formData.append("duration", minutes);
    fetch("/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.text())
      .then((response) => {
        console.log(response)
        uploader.innerText = "Uploaded Successfully !"
        uploader.style.color = "green";
      });
  });
});

// Audio file validation
const errorMessage = document.getElementById("error-message");
const sizeMessage = document.getElementById("size-message");
const transcribeButton = document.getElementById("transcribe");
const translateButton = document.getElementById("translate");
audioFile.addEventListener("change", function () {
  const file = audioFile.files[0];
  const obj = URL.createObjectURL(file);
  let fileSize = file.size;
  fileSize = fileSize/(1024*1024);
  if (fileSize>25){
    sizeMessage.style.color = 'red';
    sizeMessage.style.display = "flex";
    transcribeButton.disabled = true;
    translateButton.disabled = true;
  }else{
    transcribeButton.disabled = false;
    translateButton.disabled = false;
    sizeMessage.style.display = 'none';
  }
  audioFilePlayer.src = obj;
  const fileExtension = file.name.split(".").pop().toLowerCase();
  const supportedExtensions = ["mp3", "wav", "ogg", "m4a"];

  if (supportedExtensions.includes(fileExtension)) {
    errorMessage.style.display = "none";
    // audioPlayer.style.display = "block";
    transcribeButton.disabled = false;
    translateButton.disabled = false;
  } else {
    errorMessage.style.display = "block";
    errorMessage.style.color = "red";
    // audioPlayer.style.display = "none";
    transcribeButton.disabled = true;
    translateButton.disabled = true;
  }
});

document
  .getElementById("upload-form")
  .addEventListener("submit", function (event) {
    // prevent the default form submission behavior
    event.preventDefault();
  });


// Getting Function output through WhisperAI endpoint in python
const formData = new FormData()

function WhisperAITranscribe() {
  // Collect user input data
  // Send HTTP request to Python backend
  formData.append('task','transcribe');
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/whisper-results");
  xhr.timeout = 3000000; // Set timeout to 5 minutes in milliseconds
  xhr.onload = function() {
    if (xhr.status === 200) {
      console.log("Success");
      const data = JSON.parse(xhr.responseText);
      // Update HTML with output data returned by Python function
      const outputData = document.getElementById("outputData");
      const language_detect = document.getElementById("language_detect");
      const loader = document.getElementById("loader");
      const minutesUpdate = document.getElementById('minutesUpdate');
      const ouputDisplay = document.getElementById('outputToggle');

      ouputDisplay.style.display = 'flex';
      loader.style.display = 'none';
      outputData.innerHTML = data.outputData;
      // translated.innerHTML += '';
      language_detect.innerHTML = "Detected Language : "+data.language_detect;
      minutesUpdate.innerHTML = data.minutes_count +" / "+ data.minutes_total;
      // console.log(data)
    } else {
      console.log("Request failed");
    }
  };
  xhr.onerror = function() {
    console.log("Error");
  };
  xhr.ontimeout = function() {
    console.log("Request timed out");
  };
  xhr.send(formData);
}

const formData2 = new FormData()
function WhisperAITranslate() {
  // Collect user input data
  // Send HTTP request to Python backend
  formData2.append('task','translate');
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/whisper-results");
  xhr.timeout = 3000000; // Set timeout to 5 minutes in milliseconds
  xhr.onload = function() {
    if (xhr.status === 200) {
      console.log("Success");
      const data = JSON.parse(xhr.responseText);
      // Update HTML with output data returned by Python function
      const translated = document.getElementById("translated");
      const language_detect = document.getElementById("language_detect");
      const loader = document.getElementById("loader");
      const minutesUpdate = document.getElementById('minutesUpdate');
      const ouputDisplay = document.getElementById('outputToggle');

      ouputDisplay.style.display = 'flex';
      loader.style.display = 'none';
      // outputData.innerHTML += '';
      translated.innerHTML = data.translate;
      language_detect.innerHTML = "Detected Language : ";
      minutesUpdate.innerHTML = data.minutes_count +" / "+ data.minutes_total;
      // console.log(data)
    } else {
      console.log("Request failed");
    }
  };
  xhr.onerror = function() {
    console.log("Error");
  };
  xhr.ontimeout = function() {
    console.log("Request timed out");
  };
  xhr.send(formData2);
}


