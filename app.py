from flask import Flask,render_template,Response, session, request, redirect, url_for
import os
from dotenv import load_dotenv


app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)