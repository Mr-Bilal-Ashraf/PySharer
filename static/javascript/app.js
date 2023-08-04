var header = document.getElementById("header");
if (header.childElementCount == 4) {
  header.style.justifyContent = "space-between !important";
} else if (header.childElementCount == 3) {
  if (screen.width < 775) {
    header.setAttribute("style", "justify-content:center !important;");
  }
}

let actualBtn = document.getElementById("file");
let submitButton = document.getElementById("submit");
let fileIcon = document.getElementById("upload-icon");
let fileName = document.getElementById("file-name");
let fileType = document.getElementById("file-type");
let fileSize = document.getElementById("file-size");

actualBtn.addEventListener("change", function () {
  submitButton.style.display = "block";
  fileIcon.style.transition = "0.3s ease";
  file = this.files[0].name;
  fileName.textContent = file;
  fileTypeIndex = this.files[0].name.lastIndexOf(".");
  fileType.textContent = file.slice(fileTypeIndex + 1).toUpperCase();
  fileSize.textContent = handleFileChange();
});

function handleFileChange() {
  const fileInput = document.getElementById("file");
  const fileSizeElement = document.getElementById("fileSize");

  if (fileInput.files.length > 0) {
    const selectedFile = fileInput.files[0];
    const fileSize = selectedFile.size; // File size in bytes

    // Convert bytes to a more human-readable format
    const fileSizeFormatted = formatFileSize(fileSize);
    return fileSizeFormatted;
  } else {
    fileSizeElement.textContent = "No file selected";
  }
}

function formatFileSize(bytes) {
  const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
  if (bytes === 0) return "0 Byte";
  const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
  return Math.round(bytes / Math.pow(1024, i), 2) + " " + sizes[i];
}

function show_uploadPopup() {
  let container = document.getElementById("uploadContainer1");
  container.style.height = "100vh";
  container.style.width = "100vw";
}
function close_uploadPopup() {
  let container = document.getElementById("uploadContainer1");
  container.style.height = "0vh";
  container.style.width = "0vw";
}

function show_file_size(name, size) {
  document.getElementById("file_size_box").style.display = "flex";
  document.getElementById("file_name").innerText = name;
  document.getElementById("file_size").innerText = size;
}

function hide_file_size() {
  document.getElementById("file_size_box").style.display = "none";
}
