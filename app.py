from flask import Flask, render_template

import os
from google import genai

# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

app = Flask("SRE Helper")


@app.route("/")
def index():
    client = genai.Client(api_key=os.environ["SRE_HELPER_GEMINI_API_KEY"])
    prompt = "Explain how AI works" + "."
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"{prompt} Respond in html, ignoring the body and head tags."
    )
    return render_template("index.html", res=response.text)


app.run(host="0.0.0.0", port=5002)
