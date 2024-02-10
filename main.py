# We need to monkey_patch everything
from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask_cors import CORS

import views.index as index
import os

#Initialise FLASK app
app = Flask(__name__)

SECRET_KEY = os.environ['SECRET_KEY']

app.secret_key = SECRET_KEY
app.config['SECRET_KEY'] = SECRET_KEY

cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAX_CONTENT_LENGTH'] = 30*1024*1024 #Mb = 1024*1024 (Max of 30MByte)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000

indexview = index.indexView(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)