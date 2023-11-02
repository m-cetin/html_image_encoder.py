import os
import re
import requests
import base64
import sys

# Function to convert an image to base64
def convert_image_to_base64(url):
    """
    Converts an image to base64.

    Args:
        url: The URL of the image.

    Returns:
        A string containing the base64 encoded image data.
    """

    if url.startswith("http://") or url.startswith("https://"):
        response = requests.get(url)
        if response.status_code == 200:
            data = base64.b64encode(response.content).decode('utf-8')
            return f'data:{response.headers["Content-Type"]};base64,{data}'
        else:
            return None
    else:
        with open(url, 'rb') as file:
            data = base64.b64encode(file.read()).decode('utf-8')
            return f'data:{get_content_type(url)};base64,{data}'

# Function to get the content type of a file
def get_content_type(filename):
    """
    Gets the content type of a file.

    Args:
        filename: The name of the file.

    Returns:
        A string containing the content type of the file.
    """

    ext = os.path.splitext(filename)[1]
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

# Function to process an HTML file and convert all images to base64
def process_html_file(input_file):
    """
    Processes an HTML file and converts all images to base64.

    Args:
        input_file: The name of the HTML file.
    """

    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    pattern = r'(src|href)="(http[s]?://[^"]+|[^"]+\.(png|jpeg|jpg|gif|css|js))"'
    replaced_content = re.sub(pattern, convert_image_to_base64, html_content)

    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(replaced_content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python html_image_encoder.py <HTML file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("The specified HTML file does not exist.")
        sys.exit(1)

    process_html_file(input_file)
    print("Done!")
