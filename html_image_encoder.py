import os
import re
import requests
import base64
import sys

def replace_with_base64(match):
    attribute = match.group(1)  # src or background
    url = match.group(2)  # URL or file path

    if url.startswith("http://") or url.startswith("https://"):
        response = requests.get(url)
        if response.status_code == 200:
            data = base64.b64encode(response.content).decode('utf-8')
            return f'{attribute}="data:{response.headers["Content-Type"]};base64,{data}"'
        else:
            return match.group(0)
    else:
        with open(url, 'rb') as file:
            data = base64.b64encode(file.read()).decode('utf-8')
            return f'{attribute}="data:{get_content_type(url)};base64,{data}"'

def get_content_type(filename):
    ext = os.path.splitext(filename)[1]
    # define more extensions if needed
    if ext == ".png":
        return "image/png"
    elif ext in [".jpeg", ".jpg"]:
        return "image/jpeg"
    elif ext == ".gif":
        return "image/gif"
    elif ext == ".css":
        return "text/css"
    elif ext == ".js":
        return "application/javascript"
    else:
        return "application/octet-stream"

def process_html_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Replace all src and background images with their base64 encoded equivalent
    pattern = r'(src|background|data-thumb)="((http[s]?://[^"]+|[^"]+\.(png|jpeg|jpg|gif|css|js)))"' # here you can add more tags rather than 'src', 'background' or 'data-thumb'
    replaced_content = re.sub(pattern, replace_with_base64, html_content)

    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(replaced_content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python base64_converter.py <HTML file>")
    else:
        input_file = sys.argv[1]
        if not os.path.exists(input_file):
            print("The specified HTML file does not exist.")
        else:
            process_html_file(input_file)
            print("Done!")
