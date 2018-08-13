# Spelling Practice

The spelling practice application helps kids learn and practice 
spelling up to 10 vocabulary words at a time.

The user inputs the spelling words or chooses the words saved from the 
last session. It uses the HTML5 SpeechSynthesis API for reading each word
to be spelled. The user's answers are checked and results
of the practice test are displayed.

## Prerequisites

1. Install **python 3.6.3**.
2. Clone the github repository [spelling-practice](https://github.com/czar3985/spelling-practice).
```
$ git clone https://github.com/czar3985/spelling-practice.git
```

## Usage

**Server side:**
Run the python script _spelling_practice.py_. The following resource 
gives more information on how to run python scripts: 
[How to Run a Python Script via a File or the Shell](https://www.pythoncentral.io/execute-python-script-file-shell/).

**Client side:**
Navigate to port 8000 of the server PC
Ex: http://TEACHERPC:8000/

_words.txt_ contains the previously saved spelling words.

**Heroku page:**
The application is also deployed in http://spellingpractice.herokuapp.com/.

