from login import app
import socket


DEBUG = False
LOCAL_NETWORK = True


if __name__ == "__main__":
    if LOCAL_NETWORK:
        ip = socket.gethostbyname(socket.gethostname())
        app.run(host=ip, port=5000, debug=DEBUG)
    else:
        app.run(debug=DEBUG)
