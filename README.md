# Career Quest- Integrating NLP Chatbot into Web Application
This is my Final Year Academic Project.
## Initial Setup:

Clone repo and create a virtual environment
```
$ git clone https://github.com/selvan01/Career Quest-Job Recommender.git
$ cd Job-Recommender
$ python3 -m venv venv
$ . venv/bin/activate
```
Install dependencies
```
$ (venv) pip install Flask torch torchvision nltk
```
Install nltk package
```
$ (venv) python
>>> import nltk
>>> nltk.download('punkt')
```
Modify `intents.json` with different intents and responses for your Chatbot

Run
```
$ (venv) python train.py
```
This will dump data.pth file. And then run
the following command to test it in the console.
```
$ (venv) python chat.py
```

To run this app locally :
```
$ (venv) python app.py
```
open: localhost:127.0.0.1:5000
