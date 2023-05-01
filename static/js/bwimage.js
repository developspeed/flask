const previewImage = (event) => {
    const imageFiles = event.target.files;
    const imageFilesLength = imageFiles.length;
    const imageFilesSize = ((imageFiles[0].size)/(1024*1024)).toFixed(2);
    const size = document.getElementById('size');
    if (imageFilesLength > 0) {
      const imageSrc = URL.createObjectURL(imageFiles[0]);
      const imagePreviewElement = document.querySelector(
        "#preview-selected-image"
      );
      size.style.display = 'flex';
      size.innerHTML = "Size - "+imageFilesSize +" MB";
      imagePreviewElement.src = imageSrc;
      imagePreviewElement.style.display = "block";
      // console.log(imageFiles[0]);
    }
  
    let formData = new FormData();
    formData.append("imageFile", imageFiles[0]);
    fetch("/upload-image", {
      method: "POST",
      body: formData,
    }).then((response) => {
      console.log("Done");
    });
  };
  