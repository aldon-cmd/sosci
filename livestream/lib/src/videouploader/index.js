'use strict';


class VideoUploader{

    constructor(upload_url,csrf_token){
        this.upload_url = upload_url;
        this.csrf_token = csrf_token;
        this.upload          = null;
        this.uploadIsRunning = false;
        this.toggleBtn       = document.querySelector("#toggle-btn");
        this.resumeCheckbox  = document.querySelector("#resume");
        this.video_file_input = window.$("input[name=video_file]");
        this.progressBar     = document.querySelector(".progress-bar");
        this.alertBox        = document.querySelector("#support-alert");
        this.uploadList      = document.querySelector("#upload-list");
        this.endpointInput   = document.querySelector("#endpoint");


        if (!window.tus.isSupported) {
          alertBox.classList.remove("hidden");
        }

        if (!this.toggleBtn) {
          throw new Error("Toggle button not found on this page. Aborting upload-demo. ");
        }

        this.toggleBtn.addEventListener("click", (e) => {
          e.preventDefault();

          this.create_video();
        });
  }




 create_video(){
    var file = this.video_file_input.prop("files")[0];
    var course_module_form_data = {}; 
    window.$("#course-module-form").serializeArray().forEach(function(x){course_module_form_data[x.name] = x.value;});

    window.$.ajax({
      url: this.upload_url,
      method: "POST",
      dataType: "json",
      data: {
              name: course_module_form_data.name,
              duration: course_module_form_data.duration,
              file_size: file.size,
              csrfmiddlewaretoken: this.csrf_token
            }
  }).done((data, textStatus, jqXHR) => {

    if (this.upload) {
      if (this.uploadIsRunning) {
        this.upload.abort();
        this.toggleBtn.textContent = "resume upload";
        this.uploadIsRunning = false;
      } else {
        this.upload.start();
        this.toggleBtn.textContent = "pause upload";
        this.uploadIsRunning = true;
      }
    } else {
      if (this.video_file_input.prop("files").length > 0) {
        this.start_upload(data.upload.upload_link);
      } else {
        this.video_file_input.click();
      }
    }

    
  });
}

 start_upload(upload_link) {
  var file = this.video_file_input.prop("files")[0];
  // Only continue if a file has actually been selected.
  // IE will trigger a change event even if we reset the input element
  // using reset() and we do not want to blow up later.
  if (!file) {
    return;
  }

  var chunkSize = 100 * 1024 * 1024;

  this.toggleBtn.textContent = "pause upload";

  var options = {
    endpoint: upload_link,
    uploadUrl: upload_link,
    resume  : true,
    uploadSize: file.size,
    chunkSize: chunkSize,
    retryDelays: [0, 1000, 3000, 5000],
    metadata: {
      filename: file.name,
      filetype: file.type
    },
    onError : (error) => {
      if (error.originalRequest) {
        if (window.confirm("Failed because: " + error + "\nDo you want to retry?")) {
          this.upload.start();
          this.uploadIsRunning = true;
          return;
        }
      } else {
        window.alert("Failed because: " + error);
      }

      this.reset();
    },
    onProgress: (bytesUploaded, bytesTotal) => {
      var percentage = (bytesUploaded / bytesTotal * 100).toFixed(2);
      this.progressBar.style.width = percentage + "%";
      console.log(bytesUploaded, bytesTotal, percentage + "%");
    },
    onSuccess: () => {
      var anchor = document.createElement("a");
      anchor.textContent = "Download " + this.upload.file.name + " (" + this.upload.file.size + " bytes)";
      anchor.href = this.upload.url;
      anchor.className = "btn btn-success";
      this.uploadList.appendChild(anchor);

      this.reset();
      location.reload();
    }
  };

  this.upload = new tus.Upload(file, options);
  this.upload.start();
  this.uploadIsRunning = true;
}

 reset() {
  this.video_file_input.value = "";
  this.toggleBtn.textContent = "start upload";
  this.upload = null;
  this.uploadIsRunning = false;
}  

}


window.VideoUploader = VideoUploader;