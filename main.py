from PIL import Image
import io
import requests

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
    "prompt": "a young 17 aged male software developer from India, looking at pc, asthenic image, 4k, ultra hd, cool looks",
    "output_format": "bytes",
    "user_profile_id": "null",
    "anonymous_user_id": "a584e30d-1996-4598-909f-70c7ac715dc1",
    "request_timestamp": "1715704441.446",
    "user_is_subscribed": "false",
    "client_id": "pSgX7WgjukXCBoYwDM8G8GLnRRkvAoJlqa5eAVvj95o"
}

# Send a POST request to the API
response = requests.post(url, headers=headers, data=data)

# Check if the request was successful
if response.status_code == 200:
    # Open the image from the response content
    image = Image.open(io.BytesIO(response.content))

    # Save the image to a file
    image.save("img.png")
    print("Image saved successfully.")
else:
    # Print an error message if the request failed
    print("Failed to fetch image. Status code:", response.status_code)
