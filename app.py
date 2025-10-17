
from flask import Flask, request, jsonify, render_template
import os
import openai
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api/check', methods=['POST'])
def check_symptoms():
    data = request.get_json()
    symptoms = data.get('symptoms', '')

    if not symptoms:
        return jsonify({"error": "Please enter symptoms."}), 400

    prompt = f"Based on these symptoms: {symptoms}, suggest possible medical conditions and next steps. Include an educational disclaimer."

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150
    )

    return jsonify({"result": response.choices[0].text.strip()})

if __name__ == '__main__':
    app.run(debug=True)
