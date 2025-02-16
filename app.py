from flask import Flask, render_template, request

import os
from google import genai
from google.genai import types

# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

prompts = [
    "As a Site Reliability Engineer, how do you diagnose and handle high CPU load on production systems? Provide best practices for monitoring, alerting, and remediation.",
    "As a Site Reliability Engineer, how do you troubleshoot disk space issues? Provide steps for diagnosing, monitoring, and preventing disk exhaustion.",
    "What are the best practices for handling high network load as a Site Reliability Engineer? Include guidance on identifying bottlenecks, monitoring traffic, and optimising performance.",
    "As a Site Reliability Engineer, how do you address memory-related performance issues? Provide advice on monitoring, diagnosing memory leaks, and optimising usage."
]

app = Flask("SRE Helper")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/advice", methods=['POST'])
def advice():
    prompt_selection = request.form.get("prompt-selection")

    prompt_map = {
        "cpu": 0,
        "disk": 1,
        "network": 2,
        "memory": 3
    }

    print(f"prompt_map: {prompt_map[prompt_selection]}")

    client = genai.Client(api_key=os.environ["SRE_HELPER_GEMINI_API_KEY"])
    prompt = prompts[prompt_map[prompt_selection]]

    print(f"prompt: {prompts[prompt_map[prompt_selection]]}")

    # if prompt is None:
    #     return "Invalid selection", 400

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{prompt}",
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a staff senior reliability engineer who is giving advice to your juniors",
                "Format your entire response using valid HTML, including headers, paragraphs, and lists.",
                "Ensure the content is user-friendly and professional. Add colours and modern UI styling to make the content captivating."
            ),
            response_mime_type="text/plain"
        )
    )
    # Strip leading/trailing code block markers if present
    cleaned_response = (response.text.lstrip("```html")).rstrip("```")
    return render_template("advice.html", res=cleaned_response)


app.run(host="0.0.0.0", port=5002)

#  .lstrip("```html\n")).rstrip("\n```"))
# mimetypes are `text/plain`, `application/json` and `text/x.enum
