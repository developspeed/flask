const micIcon = document.getElementById("change");
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
    const text = document.getElementById('chatPrompt');
    // console.log("Transcript:", transcript);
    text.innerHTML = transcript;
    stopRecording()
    micIcon.click()
    // Handle the recognized speech transcript here
  };

  recognition.start();
}

function stopRecording() {
  micIcon.style.color = "gray";
  recognition.stop();
  // console.log("Recording stopped");
}

const submit = document.getElementById("submit");
submit.addEventListener("click", function () {
  const loader = document.getElementById('loader');
  loader.style.display = 'flex';
  const chatPrompt = document.getElementById("chatPrompt");
  const formData = new FormData();
  formData.append("prompt", chatPrompt.value);
  // formData.append('words',)
  fetch("/chatgpt-results", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      const output = document.getElementById("output");
      const outputData = document.getElementById("outputData");
      const wordsUpdate = document.getElementById("wordsUpdate");
      wordsUpdate.innerText = data.words_count + " / " + data.words_total;
      output.style.display = "flex";
      outputData.innerText = data.output;
      loader.style.display = 'none';
    })
    .catch((error) => {
      console.error("Error:", error);
      const outputData = document.getElementById("outputData");
      const output = document.getElementById("output");
      output.style.display = "flex";
      outputData.innerHTML = "There is some problems in prompt";
      loader.style.display = 'none';
    });
});
