# Spelling Practice

The spelling practice application helps kids learn and practice 
spelling up to 10 vocabulary words at a time.

The user inputs the spelling words or chooses the words saved from the 
last session. The website then helps set up the text to be read
by an [online text-to-speech application](https://www.text2speech.org/).
The user inputs the answers to the Spelling Practice webpage and results
of the practice test is displayed

![Spelling Practice website](./screenshots.jpg?raw=true "Title")

## Prerequisites

1. Install **python 3.6.3**.
2. Clone the github repository [spelling-practice](https://github.com/czar3985/spelling-practice).
```
$ git clone https://github.com/czar3985/spelling-practice
```

## Usage

Modify these lines to indicate the server IP and port and use that in the client's
browser to connect. Currently, it is hardcoded to run in http://localhost:8000/.
```python
if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, Speller)
    httpd.serve_forever()
```

**Server side:**
Run the python script _spelling_practice.py_. The following resource 
gives more information on how to run python scripts: 
[How to Run a Python Script via a File or the Shell](https://www.pythoncentral.io/execute-python-script-file-shell/).

**Client side:**
Go to the website specified in the code modification above.
Ex: http://TEACHERPC:8000/

_words.dat_ contains the previously saved spelling words.

## License

Spelling Practice is released under the [MIT License](https://opensource.org/licenses/MIT).