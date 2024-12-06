from flask import Flask, request
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)



if __name__ == '__main__':
    app.run(debug=True)
