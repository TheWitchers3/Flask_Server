import dotenv
import os
import sys
from flask import Flask
from flask import request
from flask import jsonify
import tsaFinal

dotenv.load_dotenv()

CK = os.getenv('CONSUMER_KEY')
CS = os.getenv('CONSUMER_SECRET')
AT = os.getenv('ACCESS_TOKEN')
ATS = os.getenv('ACCESS_TOKEN_SECRET')

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome"


@app.route('/analyze')
def analyze():
    query = request.args.get('query')
    count = request.args.get('count')
    tweetsjson = tsaFinal.getAnalysis(ck=CK, cs=CS, at=AT, ats=ATS)
    print("...tweets fetched!")
    print(tweetsjson)
    if (tweetsjson == None or (not tweetsjson)):
        errors = []
        errors.append({'text': "something went wrong!"})
        return jsonify(errors)
    return jsonify(tweetsjson)


if (__name__ == "__main__"):
    app.run()
