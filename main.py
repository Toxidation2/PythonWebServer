from http.server import BaseHTTPRequestHandler, HTTPServer
from io import StringIO
import sys
import os

hostName = "127.0.0.1"
serverPort = 80
htDocsDir = "htdocs"
defaultDocuments = ["index.py", "index.html"]
page404s = ["404.py", "404.html"]
types = [
    ["py", "py"],
    ["text/html", "html"]
]
defaultType = "text/plain"
indexingEnabled = False

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if os.path.isdir(htDocsDir + self.path):
            oldDefaultDocument = None
            for newDefaultDocument in defaultDocuments:
                if os.path.isfile(htDocsDir + self.path + "/" + newDefaultDocument):
                    oldDefaultDocument = htDocsDir + self.path + "/" + newDefaultDocument
                    break
            if oldDefaultDocument:
                fileNameAndFileExtension = os.path.splitext(oldDefaultDocument)
                newFileExtension = fileNameAndFileExtension[1]
                newFileExtension = newFileExtension.replace(".", "")
                newContentType = defaultType
                for contentTypeAndFileExtension in types:
                    oldContentType = contentTypeAndFileExtension[0]
                    oldFileExtension = contentTypeAndFileExtension[1]
                    if oldFileExtension == newFileExtension:
                        newContentType = oldContentType
                        break
                if newContentType[0:2] == "py":
                    old_stdout = sys.stdout
                    sys.stdout = mystdout = StringIO()
                    file = open(oldDefaultDocument, "r")
                    content = file.read()
                    file.close()
                    exec(content)
                    sys.stdout = old_stdout
                    content = mystdout.getvalue()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes(content, "utf-8"))
                else:
                    file = open(oldDefaultDocument, "r")
                    content = file.read()
                    file.close()
                    self.send_response(200)
                    self.send_header("Content-Type", newContentType)
                    self.end_headers()
                    self.wfile.write(bytes(content, "utf-8"))
                   
            else:
                if indexingEnabled:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes("<html><head><title>Index of " + self.path + "</title></head><body>", "utf-8"))
                    self.wfile.write(bytes("<h1>Index of " + self.path + "</h1><hr><pre>", "utf-8"))
                    directoryAndFileList = os.listdir(htDocsDir + self.path)
                    for directoryOrFile in directoryAndFileList:
                        if os.path.isdir(htDocsDir + self.path + "/" + directoryOrFile):
                            self.wfile.write(bytes("<a href=\"" + directoryOrFile + "/\">" + directoryOrFile + "/</a><br>", "utf-8"))
                        else:
                            self.wfile.write(bytes("<a href=\"" + directoryOrFile + "\">" + directoryOrFile + "</a><br>", "utf-8"))
                            
                    self.wfile.write(bytes("</pre><hr></body></html>", "utf-8"))
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes("<html><head><title>403 Forbidden</title></head><body><center><h1>403 Forbidden</h1></center><hr><center>Python</center></body></html>", "utf-8"))
        else:
            if os.path.isfile(htDocsDir + self.path):
                fileNameAndFileExtension = os.path.splitext(htDocsDir + self.path)
                newFileExtension = fileNameAndFileExtension[1]
                newFileExtension = newFileExtension.replace(".", "")
                newContentType = defaultType
                for contentTypeAndFileExtension in types:
                    oldContentType = contentTypeAndFileExtension[0]
                    oldFileExtension = contentTypeAndFileExtension[1]
                    if oldFileExtension == newFileExtension:
                        newContentType = oldContentType
                        break
                if newContentType[0:2] == "py":
                    old_stdout = sys.stdout
                    sys.stdout = mystdout = StringIO()
                    file = open(htDocsDir + self.path, "r")
                    content = file.read()
                    file.close()
                    exec(content)
                    sys.stdout = old_stdout
                    content = mystdout.getvalue()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes(content, "utf-8"))
                else:
                    file = open(htDocsDir + self.path, "r")
                    content = file.read()
                    file.close()
                    self.send_response(200)
                    self.send_header("Content-Type", newContentType)
                    self.end_headers()
                    self.wfile.write(bytes(content, "utf-8"))
            else:
                old404Page = None
                for new404Page in page404s:
                    if os.path.isfile(htDocsDir + "/" + new404Page):
                        old404Page = htDocsDir + "/" + new404Page
                        break
                if old404Page:
                    file = open(old404Page, "r")
                    content = file.read()
                    file.close()
                    self.send_response(404)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes(content, "utf-8"))
                else:
                    self.send_response(404)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes("<html><head><title>404 Not Found</title></head><body bgcolor=\"white\"><center><h1>404 Not Found</h1></center><hr><center>Python</center></body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
