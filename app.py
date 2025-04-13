from flask import Flask, request, jsonify
from flask_cors import CORS
from google.generativeai import GenerativeModel, configure

app = Flask(__name__)
CORS(app)

configure(api_key="AIzaSyAfqAsI60vWqJmXqjgZzCHrFka5cjhv4FI")
model = GenerativeModel("gemini-2.0-flash")

@app.route("/generate_quiz", methods=["POST"])
def generate_quiz():
    data = request.get_json()
    role = data.get("role")
    level = data.get("level")
    tech_stack = data.get("tech")
    count = data.get("count", 5)

    prompt = (
        f"Generate a {count}-question multiple-choice quiz for a {level}-level {role} role, "
        f"focused on {tech_stack}. Each question should have 4 options labeled A-D, with only one correct answer. "
        f"Also, provide the correct answer and a brief explanation after each question. Format:"
        f"1. [Question]\nA) Option 1\nB) Option 2\nC) Option 3\nD) Option 4\nAnswer: [Correct Option Letter]\nExplanation: [Brief explanation]\n"
    )

    response = model.generate_content(prompt)
    result = response.text

    return jsonify({"quiz": result})

@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():
    data = request.get_json()
    user_answers = data.get("answers")  # Example: {"1": "B", "2": "A", ...}
    correct_answers = data.get("correct_answers")  # Example: {"1": "B", "2": "C", ...}

    score = sum(1 for qid in correct_answers if user_answers.get(qid) == correct_answers[qid])
    total = len(correct_answers)

    return jsonify({"score": score, "total": total})

if __name__ == "__main__":
    app.run(debug=True)
