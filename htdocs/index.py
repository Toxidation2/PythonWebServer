if method == "POST":
    import cgi
    form = cgi.FieldStorage(fp = self.rfile, headers = self.headers, environ = {"REQUEST_METHOD": "POST"})
    file = open("htdocs/index.txt", "r")
    content = file.read()
    file.close()
    file = open("htdocs/index.txt", "w+")
    text = form.getvalue("text").replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    file.write(content + "<p>" + text + "</p>\n")
    file.close()
    print("<meta http-equiv=\"Refresh\" content=\"0; url='/'\">")
else:
    print("""<!doctype html>
    <html lang=\"en\">
        <head>
            <meta charset=\"utf-8\">
            <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
            <title>Hello world!</title>
            <style>
                html {
                    font-family: Verdana, Geneva, Tahoma, sans-serif;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <h1>Hello world!</h1>
            <p>Hello world!</p>
    """)
    file = open("htdocs/index.txt", "r")
    content = file.read()
    file.close()
    print(content)
    print("""
            <form method="post">
                <input type="text" name="text">
                <input type="submit">
            </form>
        </body>
    </html>""")
