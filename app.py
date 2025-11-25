import os
import google.generativeai as genai
from google.cloud import secretmanager
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Create the Secret Manager client.
client = secretmanager.SecretManagerServiceClient()

# Build the resource name of the secret version.
name = "projects/396631018769/secrets/optics-app-gemini/versions/latest"

# Access the secret version.
response = client.access_secret_version(request={"name": name})

# Extract the payload.
secret_string = response.payload.data.decode("UTF-8")


genai.configure(api_key=secret_string)
model = genai.GenerativeModel('gemini-3-pro-preview')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_fact')
def get_fact():
    try:
        prompt = "Tell me a random fun fact about golf."
        response = model.generate_content(prompt)
        return jsonify({'fact': response.text})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
