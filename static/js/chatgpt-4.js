let isRecording = false;
function micPrompt() {
  const change = document.getElementById("change");

  if (isRecording) {
    isRecording = false;
    change.style =
      "display: flex;align-items: right;justify-content: flex-end;align-items: end;z-index: 1;position: relative;top: 1rem;right: 0.3rem;color: #3aebf8";
  } else {
    isRecording = true;
    change.style =
      "display: flex;align-items: right;justify-content: flex-end;align-items: end;z-index: 1;position: relative;top: 1rem;right: 0.3rem;color: #ff0000";
  }
}

const transcript = document.getElementById("chatPrompt");
const micButton = document.getElementById("change");
// Check if the browser supports the SpeechRecognition API
if ("SpeechRecognition" in window || "webkitSpeechRecognition" in window) {
  // Create a new instance of SpeechRecognition
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

  // Set optional properties
  // recognition.lang = "en-US"; // Specify the language (e.g., 'en-US' for US English)
  recognition.continuous = true; // Enable continuous recognition

  // Handle the result event
  recognition.onresult = function(event) {
    let transcriptText = '';
    for (let i = event.resultIndex; i < event.results.length; i++) {
      if (event.results[i].isFinal) {
        transcriptText += event.results[i][0].transcript;
      }
    }
    transcript.textContent = transcriptText;

    // Perform word count on the recognized text
    const recognizedWords = transcriptText.split(/\s+/).filter(word => word !== "");
    const recognizedWordCount = recognizedWords.length;
    counter.textContent = "Words: " + recognizedWordCount;
  };
  // Handle the error event
  recognition.onerror = function (event) {
    console.error("Speech recognition error:", event.error);
  };

  let isRecognitionRunning = false;

  // Add event listener to the mic button
  micButton.addEventListener('click', () => {
    if (isRecognitionRunning) {
      // If recognition is already running, stop it
      recognition.stop();
      // micButton.textContent = 'Start';
      isRecognitionRunning = false;
    } else {
      // If recognition is not running, start it
      recognition.start();
      // micButton.textContent = 'Stop';
      isRecognitionRunning = true;
    }
  });
} else {
  console.error("Speech recognition not supported");
}

// Get the input element
const chatPrompt = document.getElementById("chatPrompt");
// Get the counter element
const counter = document.getElementById("counter");
// Add an event listener to the input element
let wordCount = 0;
chatPrompt.addEventListener("input", () => {
  const text = chatPrompt.value.trim();
  const words = text.split(/\s+/).filter((word) => word !== "");
  wordCount = words.length;

  // Update the counter element with the word count
  counter.innerText = "Words : " + wordCount;
});

const submit = document.getElementById("submit");
submit.addEventListener("click", function () {
  const loader = document.getElementById('loader');
  loader.style.display = 'flex';
  const chatPrompt = document.getElementById("chatPrompt");
  const formData = new FormData();
  formData.append("prompt", chatPrompt.value);
  formData.append("words", wordCount);
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
