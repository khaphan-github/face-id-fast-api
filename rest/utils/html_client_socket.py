HTML_CLIENT_SOCKET =  """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Face Detection with Skeleton Feedback</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }
        .container {
            display: flex;
            flex-direction: row;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .video-container {
            position: relative;
            margin-right: 20px;
        }
        #video {
            border-radius: 10px;
        }
        .face-overlay {
            position: absolute;
            border: 2px solid #00ff00;
            border-radius: 5px;
        }
        .skeleton-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 300px;
        }
        .skeleton-face {
            width: 150px;
            height: 150px;
            background-color: #e0e0e0;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
            position: relative;
        }
        .skeleton-face::before {
            content: "";
            width: 80px;
            height: 80px;
            background-color: #b0b0b0;
            border-radius: 50%;
        }
        .checkbox-button {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: 2px solid #ccc;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: background-color 0.3s, border-color 0.3s;
        }
        .checkbox-button.success {
            background-color: #28a745;
            border-color: #218838;
        }
        .checkbox-button.failure {
            background-color: #dc3545;
            border-color: #c82333;
        }
        .checkbox-button::after {
            content: "✔";
            color: white;
            font-size: 18px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        .checkbox-button.success::after,
        .checkbox-button.failure::after {
            opacity: 1;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="video-container">
            <video id="video" width="320" height="240" autoplay></video>
            <canvas id="canvas" width="320" height="240" style="display:none;"></canvas>
        </div>
        <div class="skeleton-container">
            <div class="skeleton-face"></div>
            <div id="checkbox" class="checkbox-button"></div>
        </div>
    </div>

    <script>
        var ws = new WebSocket("ws://localhost:8000/ws");

        // Handle WebSocket messages
        ws.onmessage = function(event) {
            var response = JSON.parse(event.data); // Assuming the server sends JSON
            var checkbox = document.getElementById('checkbox');

            // Update checkbox based on response
            if (response.verify == '1') {
                checkbox.classList.remove('failure');
                checkbox.classList.add('success');
            } else {
                checkbox.classList.remove('success');
                checkbox.classList.add('failure');
            }
        };

        // Setup camera
        function setupCamera() {
            let video = document.getElementById('video');
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    video.srcObject = stream;
                })
                .catch(err => {
                    console.error("Error accessing camera: ", err);
                });
        }

        // Capture and send image to WebSocket server
        function captureAndSendImage() {
            let video = document.getElementById('video');
            let canvas = document.getElementById('canvas');
            let ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            let imageData = canvas.toDataURL('image/jpg'); // Convert to Base64
            ws.send(imageData);
        }

        // Start streaming images
        function startImageStreaming() {
            setInterval(captureAndSendImage, 100); // Send an image every second
        }

        setupCamera();
        startImageStreaming();
    </script>
</body>
</html>
"""