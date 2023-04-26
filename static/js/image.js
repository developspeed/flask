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
    var imgfile = new File([dataURL], 'image.jpg',{type:dataURL.type});

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
  const imageFiles = event.target.files[0];
  const imageFilesLength = imageFiles.length;
  if (imageFilesLength > 0) {
    var imageSrc = URL.createObjectURL(imageFiles);
    const imagePreviewElement = document.querySelector(
      "#preview-selected-image"
    );
    imagePreviewElement.src = imageSrc;
    imagePreviewElement.style.display = "block";
  }
  
  let formData = new FormData();
  formData.append('imageFile',imageFiles)
  fetch('/upload-image',{
    method:"POST",
    body: formData
  }).then(response =>{console.log("Done")})
};


// Submiting the Form
let submitBtn = document.getElementById('submit')

submitBtn.addEventListener('click', function(){
  let formData = new FormData();
  formData.append('imageFile',imgfile);

  fetch('/image-edit-results',{method:'POST',body:imgfile})
  .then(response => console.log("Done"))
})
