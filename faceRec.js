const enterPass = document.getElementById('enterPass');
const face = document.getElementById('face');
const newPass = document.getElementById('newPass');
const validpass = document.getElementById('validPass');
const changePass = document.getElementById('changePass');
const change = document.getElementById('change');
const cancel = document.getElementById('cancel');
const webcam = document.getElementById('webcam');
const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');

function startWebcam() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            webcam.srcObject = stream;
            webcam.style.display = 'block';
            startFrameCapture();
        })
        .catch((error) => {
            console.error('Error accessing the webcam:', error);
        });
}

// Pass the function reference instead of invoking it immediately
face.onclick = startWebcam;

let captureInterval;

function startFrameCapture() {
    captureInterval = setInterval(() => {
        if (webcam.srcObject) {
            captureAndSendFrame(); // Send frame to server
        }
    }, 1000); // Capture every second
}

function captureAndSendFrame() {
    // Set the canvas size to match the webcam video dimensions
    canvas.width = webcam.videoWidth;
    canvas.height = webcam.videoHeight;

    // Draw the current frame from the video onto the canvas
    context.drawImage(webcam, 0, 0, canvas.width, canvas.height);

    // Convert the canvas content to a data URL (base64-encoded PNG image)
    const dataURL = canvas.toDataURL("image/png");

    // Send the image data to the Flask server via POST request
    fetch('/detect_face', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: dataURL }) // Send the image as a JSON object
    })
    .then(response => response.json())
    .then(data => {
        // Check if the server detected a face
        if (data.face_detected) {
            // If a face is detected, stop the interval and take another action
            clearInterval(captureInterval);  
            captureAndSendImage(dataURL); // Capture and send the image again if needed
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function captureAndSendImage(imageData) {
    fetch('/recognize_face', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.name); // Show the recognized face name
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function validPass(value) {
    let tries = JSON.parse(sessionStorage.getItem('tryPass')) || 5;
    const storedPassword = JSON.parse(localStorage.getItem('password')) || '1234';

    if (value.length === storedPassword.length) {
        enterPass.disabled = true;
        if (value === storedPassword) {
            enterPass.style.background = 'green';
            validpass.style.color = 'green';
            validpass.innerText = 'Correct password';

            setTimeout(() => {
                enterPass.disabled = false;
                location.reload();
            }, 1000);
        } else {
            tries--;
            enterPass.style.background = 'red';
            validpass.style.color = 'red';
            validpass.innerText = 'Wrong password!!';

            if (tries <= 0) {
                sessionStorage.setItem('tryPass', JSON.stringify(4));
                validpass.innerText = 'Wait 30 secs to try again';

                setTimeout(() => {
                    enterPass.disabled = false;
                    location.reload();
                }, 30000);
            } else {
                sessionStorage.setItem('tryPass', JSON.stringify(tries));
                setTimeout(() => {
                    enterPass.disabled = false;
                    location.reload();
                }, 1000);
            }
        }
    }
}

enterPass.addEventListener('input', () => {
    validPass(enterPass.value);
});

changePass.addEventListener('click', () => {
    change.classList.remove('hide');
});

document.getElementById('confirm').addEventListener('click', () => {
    localStorage.setItem('password', JSON.stringify(newPass.value));
    change.classList.add('hide');
});

cancel.addEventListener('click', () => {
    change.classList.add('hide');
    enterPass.value = '';
});
