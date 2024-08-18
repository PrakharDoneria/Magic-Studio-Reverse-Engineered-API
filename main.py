from flask import Flask, request, jsonify
import requests
import io
import os

app = Flask(__name__)

# Retrieve the API key from environment variables
IMGBB_API_KEY = os.getenv('IMGBB_API_KEY')

def generate_image(prompt):
    # Define the API endpoint
    url = "https://ai-api.magicstudio.com/api/ai-art-generator"

    # Define headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://magicstudio.com",
        "Referer": "https://magicstudio.com/ai-art-generator/",
    }

    # Define the data payload with the prompt and other required information
    data = {
        "prompt": prompt,
        "output_format": "bytes",
        "user_profile_id": "null",
        "anonymous_user_id": "a584e30d-1996-4598-909f-70c7ac715dc1",
        "request_timestamp": "1715704441.446",
        "user_is_subscribed": "false",
        "client_id": "pSgX7WgjukXCBoYwDM8G8GLnRRkvAoJlqa5eAVvj95o"
    }

    # Send a POST request to the API
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        # Return image bytes
        return response.content
    else:
        print("Failed to fetch image. Status code:", response.status_code)
        return None

def upload_to_imgbb(image_bytes):
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": IMGBB_API_KEY
    }
    files = {
        "image": ("generated_image.png", image_bytes, "image/png")
    }
    response = requests.post(url, data=payload, files=files)
    return response.json()['data']['url']

@app.route('/imagine', methods=['GET'])
def imagine():
    prompt = request.args.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt parameter is required"}), 400
    
    # Generate the image
    image_bytes = generate_image(prompt)
    if image_bytes:
        # Upload the image to imgBB
        img_url = upload_to_imgbb(image_bytes)
        # Return the image URL
        return jsonify({"img_url": img_url})
    else:
        return jsonify({"error": "Failed to generate image"}), 500

if __name__ == '__main__':
    app.run(debug=True)
