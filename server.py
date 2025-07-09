from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "ESP32-CAM Helmet Detection is running!"

@app.route('/upload', methods=['POST'])
def upload():
    image = request.data
    with open('static/violations/uploaded.jpg', 'wb') as f:
        f.write(image)
    return jsonify({"message": "Image received"})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
