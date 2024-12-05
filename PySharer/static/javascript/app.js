function _(el) {
    return document.getElementById(el);
}

var header = _("header");
if (header.childElementCount == 4) {
    header.style.justifyContent = "space-between !important";
} else if (header.childElementCount == 3) {
    if (screen.width < 775) {
        header.setAttribute("style", "justify-content:center !important;");
    }
}

let actualBtn = _("file");
let submitButton = _("submit");
let cancelButton = _("cancel");
let fileIcon = _("upload-icon");
let fileName = _("file-name");
let fileType = _("file-type");
let fileSize = _("file-size");
let xhr = "";

actualBtn.addEventListener("change", function () {
    submitButton.style.display = "block";
    cancelButton.style.display = "none";
    fileIcon.style.transition = "0.3s ease";
    file = this.files[0].name;
    fileName.textContent = file;
    fileTypeIndex = this.files[0].name.lastIndexOf(".");
    fileType.textContent = file.slice(fileTypeIndex + 1).toUpperCase();
    fileSize.textContent = handleFileChange();
    status.innerHTML = "";
});

function handleFileChange() {
    const fileInput = _("file");
    const fileSizeElement = _("fileSize");

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
    let container = _("uploadContainer1");
    container.style.height = "100vh";
    container.style.width = "100vw";
}

function close_uploadPopup() {
    let container = _("uploadContainer1");
    container.style.height = "0vh";
    container.style.width = "0vw";
    bar.style.display = "none";
    submitButton.style.display = "none";
    cancelButton.style.display = "none";
    file_input.value = "";
    fileName.textContent = "- - - - ";
    fileType.textContent = "- - - - ";
    fileSize.textContent = "- - - - ";
    if (typeof (xhr) == "object") {
        xhr.abort();
    }
}

function show_file_size(name, size) {
    _("file_size_box").style.display = "flex";
    _("file_name").innerText = name;
    _("file_size").innerText = size;
}

function hide_file_size() {
    _("file_size_box").style.display = "none";
}

const form = _("uploadForm");
const file_input = _("file");
const bar = _("progressBar");
const status = _("progressStatus");

function listenXmlRequest() {
    let data = JSON.parse(this.responseText);
    console.log("Status Code -=> ", this.status);
    if (data.code == true) {
        status.innerHTML = "Uploaded Successfully!";
        setTimeout(function () {
            location.reload();
        }, 500);
    } else {
        status.innerHTML = data.message;
        actualBtn.disabled = false;
        bar.style.display = "none";
        file_input.value = "";
        fileName.textContent = "- - - - ";
        fileType.textContent = "- - - - ";
        fileSize.textContent = "- - - - ";
    }
}

form.addEventListener("submit", e => {
    e.preventDefault();
    bar.style.display = "block";
    submitButton.style.display = "none";
    cancelButton.style.display = "block";
    actualBtn.disabled = true;

    const form_data = new FormData();
    const files = file_input.files;
    for (i = 0; i < files.length; i++ ) {
        form_data.append("file", files[i]);
    }

    xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload/', true);
    xhr.upload.onprogress = e => {
        if (e.lengthComputable) {
            const percentComplete = Math.round((e.loaded / e.total) * 100);
            bar.value = percentComplete;
            status.innerText = `${percentComplete} %`;
        }
    };
    xhr.send(form_data);
    xhr.addEventListener("load", listenXmlRequest);
})

cancelButton.addEventListener("click", e => {
    xhr.abort();
    bar.style.display = "none";
    status.innerText = "Upload canceled";
    cancelButton.style.display = "none";
    actualBtn.disabled = false;
    file_input.value = "";
    fileName.textContent = "- - - - ";
    fileType.textContent = "- - - - ";
    fileSize.textContent = "- - - - ";
})

function generateQRCode(ipAddress) {
  const container = document.getElementById("qr-code-container");
  container.style.display = "block";
  container.innerHTML = ""; // Clear any existing QR code
  const qrCode = new QRCode(container, {
    text: `http://${ipAddress}`,
    width: 150,
    height: 150,
  });
}

function showQRCode(ipAddress) {
  generateQRCode(ipAddress);
  const container = document.getElementById("model-container");
  container.style.visibility = "visible";
  container.style.opacity = "1";
}
function hideQRCode() {
  const container = document.getElementById("model-container");
  container.style.visibility = "hidden";
  container.style.opacity = "0";
}
