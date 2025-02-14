from flask import Flask, render_template

import os
# Importing the necessary functions from the dotenv library.
from dotenv import load_dotenv, dotenv_values

# Loading variables from the .env file.
load_dotenv()

app = Flask("SRE Helper")

print(os.getenv("SRE_HELPER_GEMINI_API_KEY"))


@app.route("/")
def index():
    response = "Lisa"
    return render_template("index.html", res=response)


app.run(host="0.0.0.0", port=5002)
