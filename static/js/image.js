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
    
    canvas.toBlob((blob) => {
      const formData = new FormData();
      formData.append('imageFile', blob);
      fetch('/upload-image', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        console.log("Done");
      })
      .catch(error => {
        console.error(error);
      });

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

});

// const video = document.getElementById('video');
// const canvas = document.getElementById('canvas');
// const capture = document.getElementById('capture');

// const constraints = {
//   video: true
// };

// navigator.mediaDevices.getUserMedia(constraints)
// .then((stream) => {
//   video.srcObject = stream;
// })
// .catch((error) => {
//   console.error(error);
// });

// capture.addEventListener('click', () => {
//   canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
//   canvas.toBlob((blob) => {
//     const formData = new FormData();
//     formData.append('image', blob, 'image.jpg');
//     fetch('/upload-image', {
//       method: 'POST',
//       body: formData
//     })
//     .then(response => {
//       console.log(response);
//     })
//     .catch(error => {
//       console.error(error);
//     });
//   }, 'image/jpeg', 0.95);
// });





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


