import torch

def load_model():
    return torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/best.pt', force_reload=True)

def detect_helmet(model, image):
    results = model(image)
    df = results.pandas().xyxy[0]
    person = not df[df['name'] == 'person'].empty
    helmet = not df[df['name'] == 'helmet'].empty
    return helmet and person
