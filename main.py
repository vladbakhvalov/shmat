import pyaudio
from http.server import BaseHTTPRequestHandler, HTTPServer
import os


class SHMATHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # send code 200 response
        self.send_response(200)

        self.send_header("Connection", "Keep-Alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Content-Type-Options", "nosniff")
        #self.send_header("Transfer-Encoding", "chunked")
        self.send_header("Content-Type", "audio/wave")
        self.end_headers()

        CHUNK = 512

        WIDTH = 2
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 10

        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,  # p.get_format_from_width(WIDTH),
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        output=True,
                        frames_per_buffer=CHUNK)

        ##for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        while True:
            data = stream.read(CHUNK)  # read audio stream
            # stream.write(data, CHUNK)  # play back audio stream

            # send file content to client

            self.wfile.write(data)
            self.wfile.flush()
            if not data:
                break


def run():
    try:
        print('http server is starting...')
        # ip and port of servr
        # by default http server port is 80
        server_address = ('127.0.0.1', 8005)
        httpd = HTTPServer(server_address, SHMATHTTPRequestHandler)
        print('http server is running...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        httpd.socket.close()


if __name__ == '__main__':
    run()
