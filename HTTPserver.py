# coding = utf-8
from socket import *
from multiprocessing import Process


class HTTPServer(object):
    def __init__(self):
        self.HTTPServer = socket(AF_INET, SOCK_STREAM)
        self.HTTPServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.response = ""
        self.response_header = ""

    def start(self, port):
        self.HTTPServer.bind(("", port))
        self.HTTPServer.listen(5)
        try:
            while True:
                NewServer, dstSock = self.HTTPServer.accept()
                P = Process(target=self.HTTPHandle, args=(NewServer, dstSock))
                P.start()
                NewServer.close()
        except Exception as e:
            HTTPServer.close()
            print(e)

    def start_response(self, status, headers):
        #   org_headers = [("server": "my_server")]
        response_headers = "HTTP/1.1 " + status + "\r\n"
        for header in headers:
            response_headers += "%s: %s\r\n" % header
        self.response_header = response_headers
        print(self.response_header)

    def HTTPHandle(self, NewServer, dstSock):
        HTML_DIR = "."
        while True:
            data = NewServer.recv(1024)
            requestLine = data.splitlines()
            file_name = requestLine[0].split()[1]
            print(file_name)
            #   print requestLine

            if "/" == file_name:
                #   print ("recv from %s data %s" % (str(dstSock), data))
                #   print(data)
                file_name = "/index.html"
                try:
                    FILE = open(HTML_DIR+file_name, "rb")
                except IOError:
                    self.response = "HTTP/1.1 404 Not Found\r\n" + "\r\n" + "bad url"
                else:
                    responseBody = FILE.read()
                    FILE.close()
                    self.response = "HTTP/1.1 200 OK\r\n" + "\r\n" + responseBody

            else:
                if file_name.endswith(".py"):
                    try:
                        m = __import__(file_name[1:-3])
                        print(file_name[1:-3])
                    except Exception:
                        self.response = "HTTP/1.1 404 Not Found\r\n" + "\r\n" + "bad url"
                    else:
                        #   "METHOD": method,
                        #   "PATH": path
                        env = {}
                        responseBody = m.application(env, self.start_response)
                        self.response = self.response_header + "\r\n" + responseBody

            print(self.response)

            NewServer.send(self.response)
            NewServer.close()


def main():
    HTTP_OBJECT = HTTPServer()
    HTTP_OBJECT.start(8080)


if __name__ == "__main__":
    main()
