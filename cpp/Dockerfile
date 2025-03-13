# Stage 1: Build the application
FROM debian:bookworm-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive

# Install only necessary build dependencies
RUN apt update && apt install -y \
    libzmq3-dev libopencv-dev g++ cmake pkg-config && \
    rm -rf /var/lib/apt/lists/*  # Remove package lists to reduce size

WORKDIR /app

# Copy source files
COPY main.cpp /app/main.cpp
COPY haarcascade_frontalface_default.xml /app/haarcascade_frontalface_default.xml

# Compile the C++ program
RUN g++ -o main main.cpp -lzmq `pkg-config --cflags --libs opencv4` && strip main

# Stage 2: Create a minimal runtime image
FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install only runtime dependencies (not build tools)
RUN apt update && apt install -y \
    libzmq3-dev libopencv-dev && \
    rm -rf /var/lib/apt/lists/*  # Reduce image size

WORKDIR /app

# Copy the compiled binary and necessary model file
COPY --from=builder /app/main /app/main
COPY --from=builder /app/haarcascade_frontalface_default.xml /app/haarcascade_frontalface_default.xml

# Expose WebSocket port
EXPOSE 5555

# Run the application
CMD ["sh", "-c", "./main"]
