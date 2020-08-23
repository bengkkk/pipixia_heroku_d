docker build -t test . && \
docker run -d -p 8022:22 -p 8080:8888 test