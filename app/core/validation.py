import requests

def validate_url(url):
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return "Valid"
        else:
            return "Invalid"
    except requests.RequestException:
        return "Invalid"
