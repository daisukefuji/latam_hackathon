import base64
import os
import openai
import sys
import re
from ppadb.client import Client as AdbClient

class AdbScreen:
    def __init__(self, host:str="127.0.0.1", port:int=5037):
        self._host = host
        self._port = port

        client = AdbClient(host=self._host, port=self._port)
        devices = client.devices()
        if len(devices) > 1:
            serials = ",".join(device.serial for device in devices)
            raise ValueError(f"Found many devices({serials})")
        elif len(devices) == 0:
            raise ValueError(f"Not found any device")
        else:
            self._device = devices[0]

        api_key=os.environ.get("SAMBANOVA_API_KEY")
        if not api_key:
            raise ValueError("Set SAMBANOVA_API_KEY")

        self._client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.sambanova.ai/v1",
        )

    def check(self, condition:str) -> bool:
        result = self._device.screencap()
        base64_string = f"data:image/png;base64,{base64.b64encode(result).decode('utf-8')}"

        request = f"just return true if {condition} othewise return false"
        response = self._client.chat.completions.create(
            model='Llama-3.2-11B-Vision-Instruct',
            messages=[{"role":"user","content":[{"type":"text","text":request},{"type":"image_url","image_url":{"url":f"{base64_string}"}}]}],
            temperature =  0.1,
            top_p = 0.1
        )

        content = response.choices[0].message.content
        match = re.search(r'\*Answer\*: (True|False)', content)
        if match:
            return match.group(1) == "True"
        return False

def main():
    screen = AdbScreen()
    condition = "that picture contains next button"
    print(f'"{condition}" is {screen.check(condition)}')

if __name__ == "__main__":
    main()