from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

SYSTEM_PROMPT = """
You are HyCorp Internal AI Assistant.

Guidelines:
- Respond politely and professionally.
- Answer HR-related questions using HR data.
- If asked about available data, only list high-level categories.
- Do NOT reveal detailed internal infrastructure information unless the user explicitly requests that section.
- Keep responses concise.
"""

def load_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r") as f:
        return f.read()

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""

    if request.method == "POST":
        user_input = request.form["user_input"]

        hr_data = load_file("data/hr.txt")
        internal_docs = load_file("data/internal_docs.txt")

        full_prompt = f"""
{SYSTEM_PROMPT}

Company HR Data:
{hr_data}

Internal Infrastructure Documents:
{internal_docs}

User Question:
{user_input}

Answer concisely:
"""

        try:
            ai_response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": full_prompt,
                    "stream": False,
                    "temperature": 0
                }
            )

            response = ai_response.json()["response"]

        except Exception as e:
            response = f"AI Error: {str(e)}"

    return render_template("index.html", response=response)


if __name__ == "__main__":
    app.run(debug=True)