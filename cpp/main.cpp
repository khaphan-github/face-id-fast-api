#include <opencv2/opencv.hpp>
#include <zmq.hpp>
#include <iostream>
#include <chrono>
#include <iomanip>
#include <cstdlib> 

zmq::context_t context(1);
zmq::socket_t socket(context, ZMQ_REP);

std::string current_time() {
    auto now = std::chrono::system_clock::now();
    auto in_time_t = std::chrono::system_clock::to_time_t(now);
    std::stringstream ss;
    ss << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %X");
    return ss.str();
}

bool is_face_centered(cv::Mat frame, const std::vector<cv::Rect>& faces) {
    int img_height = frame.rows;
    int img_width = frame.cols;

    for (const auto& face : faces) {
        int face_center_x = face.x + face.width / 2;
        int face_center_y = face.y + face.height / 2;

        int screen_center_x = img_width / 2;
        int screen_center_y = img_height / 2;

        if (std::abs(face_center_x - screen_center_x) <= img_width * 0.1 &&
            std::abs(face_center_y - screen_center_y) <= img_height * 0.1) {
            return true;
        }
    }

    return false;
}

std::vector<cv::Rect> detect_faces(cv::Mat frame) {
    cv::CascadeClassifier face_cascade;
    
    if (!face_cascade.load("haarcascade_frontalface_default.xml")) {
        std::cerr << "[" << current_time() << "][ERROR]: Could not load face cascade file!" << std::endl;
        return {};
    }

    std::vector<cv::Rect> faces;
    face_cascade.detectMultiScale(frame, faces);

    std::vector<cv::Rect> centered_faces;
    for (const auto& face : faces) {
        if (is_face_centered(frame, {face})) {
            centered_faces.push_back(face);
        }
    }

    return centered_faces;
}

int main() {
    try {
        const char* port_env = std::getenv("PORT");
        std::string port = port_env ? port_env : "5555";

        socket.bind("tcp://*:" + port);
        std::cout << "[" << current_time() << "][START] Server started on port 5555" << std::endl;

        while (true) {
            zmq::message_t request;

            auto result = socket.recv(request, zmq::recv_flags::none);
            if (!result || *result == 0) {
                std::cerr << "[" << current_time() << "][ERROR]: Failed to receive message!" << std::endl;
                continue;
            }

            std::vector<uchar> data(request.size());
            memcpy(data.data(), request.data(), request.size());

            cv::Mat frame = cv::imdecode(data, cv::IMREAD_COLOR);
            if (frame.empty()) {
                std::cerr << "[" << current_time() << "][ERROR]: Received empty frame!" << std::endl;
                continue;
            }

            std::vector<cv::Rect> faces = detect_faces(frame);

            std::cout << "[" << current_time() << "][INFO] Faces detected: " << faces.size() << std::endl;

            std::string reply = std::to_string(faces.size());
            socket.send(zmq::message_t(reply.begin(), reply.end()), zmq::send_flags::none);
        }
    } catch (const zmq::error_t& e) {
        std::cerr << "[" << current_time() << "] ZeroMQ Error: " << e.what() << std::endl;
        return 1;
    } catch (const std::exception& e) {
        std::cerr << "[" << current_time() << "] Exception: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
