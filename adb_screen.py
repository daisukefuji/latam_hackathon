import base64
import os
import openai
import sys
import re
from ppadb.client import Client as AdbClient

def main():
    condition = "that picture contains next button and red pin"
    print(f'"{condition}" is {check(condition)}')

def check(condition:str) -> bool:
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    #for device in devices:
    #    print(device.serial)
    result = devices[0].screencap()
    base64_string = f"data:image/png;base64,{base64.b64encode(result).decode('utf-8')}"

    api_key=os.environ.get("SAMBANOVA_API_KEY")
    if not api_key:
        sys.exit("Set SAMBANOVA_API_KEY")

    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.sambanova.ai/v1",
    )

    request = f"just return true if {condition} othewise return false"
    response = client.chat.completions.create(
        model='Llama-3.2-11B-Vision-Instruct',
        messages=[{"role":"user","content":[{"type":"text","text":request},{"type":"image_url","image_url":{"url":f"{base64_string}"}}]}],
        temperature =  0.1,
        top_p = 0.1
    )

    content = response.choices[0].message.content
    match = re.search(r'\*Answer\*: (True|False)', content)
    if match:
        return match.group(1) == "True"
    else:
        return False

if __name__ == "__main__":
    main()