#!/usr/bin/env python3
#
# A *spelling server* for spelling practice
#

import http.server
import requests
import os
from urllib.parse import unquote, parse_qs

words = []
answers = []


def OpenCSSFile(self):
    # Send a 200 OK response.
    self.send_response(200)

    # Send headers.
    self.send_header('Content-type', 'text/css')
    self.end_headers()

    # Send the response.
    css_file = open("main.css")
    self.wfile.write(css_file.read().encode())
    css_file.close()


def OpenJSFile(self):
    # Send a 200 OK response.
    self.send_response(200)

    # Send headers.
    self.send_header('Content-type', 'text/javascript')
    self.end_headers()

    # Send the response.
    js_file = open("main.js", encoding='utf-8-sig')
    self.wfile.write(js_file.read().encode())
    print(js_file.read())
    js_file.close()


def OpenIndexPage(self):
    # Send a 200 OK response.
    self.send_response(200)

    # Send headers.
    self.send_header('Content-type', 'text/html; charset=utf-8')
    self.end_headers()

    # Load html file into the response
    html_file = open('index.html', encoding='utf-8-sig')
    response = html_file.read()
    html_file.close()

    # Send the response.
    self.wfile.write(response.encode())


def OpenSetupPage(self):
    # Send a 200 OK response.
    self.send_response(200)

    # Send headers.
    self.send_header('Content-type', 'text/html; charset=utf-8')
    self.end_headers()

    # Put the response together out of the html file and the spelling words.
    # Load html file into the response
    html_file = open('setup.html', encoding='utf-8-sig')
    html_string = html_file.read()
    html_file.close()

    words_container = ''
    for index, item in enumerate(words):
        words_container += "<p>{}. {}</p>".format(str(index + 1), item)
    response = html_string.format(words_container)

    # Send the response.
    self.wfile.write(response.encode())


def OpenPracticePage(self):
    # Send a 200 OK response.
    self.send_response(200)

    # Send headers.
    self.send_header('Content-type', 'text/html; charset=utf-8')
    self.end_headers()

    # Put the response together out of the html file and the spelling words.
    # Load html file into the response
    html_file = open('practice.html', encoding='utf-8-sig')
    html_string = html_file.read()
    html_file.close()

    result_container = ''
    for index, item in enumerate(words):
        result_container += '''
            <div class="form-group row">
                <label for="answer{}" class="col-sm-1 col-form-label">{}.</label>
                <input type="button" value="Play" class="btn col-sm-1 play-button" data-speech="{}" />
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="answer{}" name="answer{}">
                </div>
            </div>
            '''.format(str(index+1), str(index+1), words[index], str(index+1), str(index+1))

    response = html_string.format(result_container)

    # Send the response.
    self.wfile.write(response.encode())


def OpenResultPage(self):
    # Send a 200 OK response.
    self.send_response(200)

    # Send headers.
    self.send_header('Content-type', 'text/html; charset=utf-8')
    self.end_headers()

    # Put the response together out of the html file and the spelling words + answers.
    # Load html file into the response
    html_file = open('result.html', encoding='utf-8-sig')
    html_string = html_file.read()
    html_file.close()

    result_container = ''
    for index, item in enumerate(words):
        if index >= len(answers): # If answers given are less than expected, put no answer
            result_container += "<p>{}. <em>No answer</em> ".format(str(index+1))
        else:
            result_container += "<p>{}. {} ".format(str(index+1), answers[index])

            if item == answers[index]:
                result_container += "<strong>Correct</strong></p>"
            else:
                result_container += "<strong class='incorrect_answer'>Incorrect</strong>. The correct spelling is {}.</p>".format(item)

    response = html_string.format(result_container)

    # Send the response.
    self.wfile.write(response.encode())


def UsePreviousWords(self):
    global words

    words = [] # Initialize to overwrite if changed
    word_file = open('words.txt','r')
    words = word_file.read().splitlines()
    word_file.close()

    if len(words) == 0:
        self.send_response(400)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("No previously saved words".encode())
        return
    else:
        #Serve a redirect to the Setup Page.
        self.send_response(303)
        self.send_header('Location', '/setup.html')
        self.end_headers()


def StartTest(self):
    # Redirect to Practice Page
    self.send_response(303)
    self.send_header('Location', '/practice.html')
    self.end_headers()


def SubmitAnswers(self, body):
    global answers

    # Parse the answers submitted
    params = parse_qs(body)

    answers = []
    params_left = len(params)
    for i in range(1, 11):
        if params_left == 0:
            break
        if "answer{}".format(str(i)) in params: # If answer was given for the nummber
            answers.append(params["answer{}".format(str(i))][0])
            params_left -= 1
        else:
            answers.append('')

    # Redirect to Result Page
    self.send_response(303)
    self.send_header('Location', '/result.html')
    self.end_headers()


def SaveNewWords(self, body):
    global words

    # Parse the answers submitted
    params = parse_qs(body)

    words = [] # Initialize so that it will get a new set everytime
    for index, item in enumerate(params):
        words.append(params["word{}".format(str(index + 1))][0])

    if len(words) == 0:
        self.send_response(400)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("Missing input".encode())
        return

    # Serve a redirect to the Setup page.
    self.send_response(303)
    self.send_header('Location', '/setup.html')
    self.end_headers()

    # Save new set of words
    word_file = open('words.txt','w')
    word_file.write("\n".join(words))
    word_file.close()


class Speller(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # A GET request will either be for / (the root path) or for /main.css.
         # Handle css file getting
        if self.path == "/main.css":
            OpenCSSFile(self)
            return

        elif self.path == "/main.js":
            OpenJSFile(self)
            return

        elif self.path == "/favicon.ico":
            return

        elif self.path == "/":
            OpenIndexPage(self)
            return

        elif self.path == "/setup.html":
            OpenSetupPage(self)
            return

        elif self.path == "/practice.html":
            OpenPracticePage(self)
            return

        elif self.path == "/result.html":
            OpenResultPage(self)
            return


    def do_POST(self):
        # Decode the form data.
        length = int(self.headers.get('Content-length', 0))
        body = self.rfile.read(length).decode()

        if 'usePrevious' in body:
            UsePreviousWords(self)
            return

        elif 'startTest' in body:
            StartTest(self)
            return

        elif 'answer' in body:
            SubmitAnswers(self, body)
            return

        elif 'word' in body:
            SaveNewWords(self, body)
            return


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))   # Use PORT if it's there.
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, Speller)
    httpd.serve_forever()
