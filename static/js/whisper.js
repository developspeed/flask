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
      let audioBlob = new Blob(chunks, { type: "audio/ogg; codecs=opus" });
      let audioUrl = URL.createObjectURL(audioBlob);
      const audioPlayer = document.getElementById("audio-player");
      const audioElement = new Audio(audioUrl);
      audioPlayer.src = audioUrl;
      let formData = new FormData();
      formData.append("audio", audioBlob);

      //   Duration Getting

      const audioContext = new AudioContext();
      const fileReader = new FileReader();
      var minutes = 0;
      fileReader.onload = function () {
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
}

startButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

// Audio Player for uploaded audio and duration to server
const audioFile = document.getElementById("audioFile");
const audioFilePlayer = document.getElementById("audio-upload-player");
audioFile.addEventListener("change", function () {
  const file = audioFile.files[0];
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
      .then((response) => console.log(response));
  });
});

// Audio file validation
const errorMessage = document.getElementById("error-message");
audioFile.addEventListener("change", function () {
  const file = audioFile.files[0];
  const obj = URL.createObjectURL(file);
  audioFilePlayer.src = obj;
  const fileExtension = file.name.split(".").pop().toLowerCase();
  const supportedExtensions = ["mp3", "wav", "ogg", "m4a"];
  const transcribeButton = document.getElementById("transcribe");
  if (supportedExtensions.includes(fileExtension)) {
    errorMessage.style.display = "none";
    // audioPlayer.style.display = "block";
    transcribeButton.disabled = false;
  } else {
    errorMessage.style.display = "block";
    errorMessage.style.color = "red";
    // audioPlayer.style.display = "none";
    transcribeButton.disabled = true;
  }
});

document
  .getElementById("upload-form")
  .addEventListener("submit", function (event) {
    // prevent the default form submission behavior
    event.preventDefault();
  });

function WhisperAI() {
  // Send HTTP request to run Python function
  fetch("/run_python_function")
    .then(function (response) {
      return response.text();
    })
    .then(function (outputData) {
      // Update outputDiv with the output of the Python function
      document.getElementById("outputDiv").innerHTML = outputData;
    });
}



const to_translate = document.getElementById("inlineCheckbox1").value;
// console.log(to_translate)
const formData = new FormData()
formData.append('to_translate',to_translate);
const maxRetries = 4; // Set maximum number of retries
let retryCount = 0;

async function WhisperAI() {
  try {
    const response = await fetch("/whisper-results", {
      method: "POST",
      body: formData,
      // timeout: 30000000 // Set timeout to 30 seconds
    });
    const data = await response.json();
    // Update HTML with output data returned by Python function
    const outputData = document.getElementById("outputData");
    const translated = document.getElementById("translated");
    const language_detect = document.getElementById("language_detect");
    const loader = document.getElementById("loader");
    const minutesUpdate = document.getElementById('minutesUpdate');
    const ouputDisplay = document.getElementById('outputToggle');

    ouputDisplay.style.display = 'flex';
    loader.style.display = 'none';
    outputData.innerHTML = data.outputData;
    translated.innerHTML = data.translate;
    language_detect.innerHTML = "Detected Language : "+data.language_detect;
    minutesUpdate.innerHTML = data.minutes_count +" / "+ data.minutes_total;
    // console.log(data)
  } catch (error) {
    // Handle the error response here
    if (error.status === 504 && retryCount < maxRetries) {
      // If the error is a 504 error and we haven't reached the maximum number of retries, retry the request
      retryCount++;
      await WhisperAI(); // Call the function again recursively
    } else {
      console.log("Failed to fetch data:", error);
    }
  }
}

WhisperAI(); // Call the function to start the request

