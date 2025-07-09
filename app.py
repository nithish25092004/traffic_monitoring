from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    file.save("uploads/" + file.filename)
    return "Image uploaded successfully"

if __name__ == '__main__':
    app.run(debug=True)
