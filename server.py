from flask import Flask, request, render_template
import cv2, numpy as np, os, pandas as pd
from datetime import datetime
from detect import load_model, detect_helmet
from send_sms import send_sms_fast2sms

app = Flask(__name__)
model = load_model()
df = pd.read_csv("database.csv")

@app.route('/upload', methods=['POST'])
def upload():
    image_data = request.data
    img_np = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("static/violations", exist_ok=True)
    fname = f"static/violations/{now}.jpg"
    cv2.imwrite(fname, img)

    helmet_ok = detect_helmet(model, img)
    person_info = df.iloc[0]
    valid_until = datetime.strptime(person_info["valid_until"], "%Y-%m-%d")
    is_expired = datetime.now() > valid_until

    with open(fname + ".txt", "w") as f:
        f.write("Helmet: No\n" if not helmet_ok else "Helmet: Yes\n")
        f.write("Papers: Expired\n" if is_expired else "Papers: Valid\n")
        f.write("SMS: Sent\n" if not helmet_ok or is_expired else "SMS: Not Sent\n")
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if not helmet_ok or is_expired:
        message = f"Alert: Helmet: {'No' if not helmet_ok else 'Yes'}, Papers: {'Expired' if is_expired else 'Valid'}"
        send_sms_fast2sms(person_info["phone"], message)
        return message
    return "Helmet and papers OK"

@app.route('/dashboard')
def dashboard():
    records = []
    files = sorted(os.listdir("static/violations"))[::-1]
    for f in files:
        if f.endswith(".jpg"):
            info = f + ".txt"
            path = os.path.join("static/violations", info)
            if os.path.exists(path):
                with open(path) as txt:
                    lines = txt.read().splitlines()
                    records.append({
                        "image": f"/static/violations/{f}",
                        "helmet": lines[0],
                        "papers": lines[1],
                        "sms": lines[2],
                        "time": lines[3],
                    })
    return render_template("dashboard.html", records=records)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
