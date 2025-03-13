
![alt text](image.png)
# Face Detection using C++ and ZeroMQ
This project face detection using OpenCV and ZeroMQ in C++. It provides a simple and efficient way to detect faces in images or video streams.

## Features
![alt text](image-1.png)
- **Real-time Face Detection**: Utilizes OpenCV's powerful face detection capabilities.
- **Message Passing**: Uses ZeroMQ for efficient message passing between different components.
- **Cross-Platform**: Can be built and run on various operating systems.

## Prerequisites

Ensure you have the following installed on your system:

- C++ compiler (e.g., g++)
- OpenCV library
- ZeroMQ library
- Docker (optional, for containerized execution)

## Installation

First, update your package list and install the required dependencies:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install libzmq3-dev libopencv-dev
```

## Build and Run

To compile and run the code, use the following commands:

```bash
g++ main.cpp -o main `pkg-config --cflags --libs opencv4` -lzmq
./main
```

## Docker

You can also build and run the project using Docker:

```bash
docker build -t face_detector_cpp .
docker run --rm -it face_detector_cpp
```

## Usage

After building the project, you can run the executable to start detecting faces. The program will process images or video streams and highlight detected faces.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.

