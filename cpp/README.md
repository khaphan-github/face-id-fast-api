
# ins
Install dependencies contain opencv and zezomq
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install libzmq3-dev libopencv-dev
```

```bash
g++ main.cpp -o main `pkg-config --cflags --libs opencv4` -lzmq
./main
```


```bash
docker build -t face_detector_cpp .

```