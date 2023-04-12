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
      const audioPlayer = document.getElementById('audio-player');
      audioPlayer.src = audioUrl;
      // audioPlayer.play();
      // let audio = new Audio(audioUrl);
      // audio.controls = true;
      // document.body.appendChild(audio);

      let formData = new FormData();
      formData.append("audio", audioBlob);

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

const audioFile = document.getElementById('audioFile');
const audioFilePlayer = document.getElementById('audio-upload-player')

audioFile.addEventListener('change', function(){
  const file = audioFile.files[0];
  const obj = URL.createObjectURL(file);
  audioFilePlayer.src = obj;
})