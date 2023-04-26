const captureButton = document.getElementById("capture");
const image = document.getElementById("image");


captureButton.addEventListener("click", function () {
  const video = document.getElementById("video");
  const photo = document.getElementById("photo");
  video.style.display = "flex";
  captureButton.innerText = "Capture";
  let stream = null;

  captureButton.addEventListener("click", () => {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);
    const dataURL = canvas.toDataURL("image/png");
    image.style.display = "flex";
    photo.setAttribute("src", dataURL);
    const base64String = dataURL.split(',')[1];

    // Decode the Base64-encoded data
    const decodedData = atob(base64String);
    console.log(decodedData)
    // Convert the decoded data to a Blob
    const blob = new Blob([decodedData], { type: 'image/png' });

    // Create a new File object from the Blob
    const imgfile = new File([blob], 'image.png', { type: 'image/png' });
    let formData = new FormData();
    formData.append('imageFile',imgfile)
    fetch('/upload-image',{
      method:"POST",
      body: formData
    }).then(response =>{console.log("Done")})
  });


  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((mediaStream) => {
      stream = mediaStream;
      video.srcObject = stream;
      video.play();
    })
    .catch((error) => {
      console.error("Unable to access camera", error);
    });

});

// For uploading and sending image to server
const previewImage = (event) => {
  const imageFiles = event.target.files;
  const imageFilesLength = imageFiles.length;
  if (imageFilesLength > 0) {
      const imageSrc = URL.createObjectURL(imageFiles[0]);
      const imagePreviewElement = document.querySelector("#preview-selected-image");
      imagePreviewElement.src = imageSrc;
      imagePreviewElement.style.display = "block";
      console.log(imageFiles[0])
  }

  
  let formData = new FormData();
  formData.append('imageFile',imageFiles[0])
  fetch('/upload-image',{
    method:"POST",
    body: formData
  }).then(response =>{console.log("Done")})
};


