import requests

def send_sms_fast2sms(phone, message):
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        'sender_id': 'TXTIND',
        'message': message,
        'language': 'english',
        'route': 'v3',
        'numbers': phone
    }
    headers = {
        'authorization': 'YOUR_FAST2SMS_API_KEY',  # Replace with your API key
        'Content-Type': "application/x-www-form-urlencoded",
    }
    response = requests.post(url, data=payload, headers=headers)
    print("SMS Response:", response.text)
