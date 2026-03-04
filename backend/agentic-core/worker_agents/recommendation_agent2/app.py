import requests
import json

class OllamaClient:
    def __init__(self, base_url="http://192.168.0.160:11434", model="qwen2.5:7b"):
        """
        Initialize the Ollama client.
        :param base_url: URL of the Ollama server (with IP and port)
        :param model: Default model to use
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.history = []  # Keeps chat history (optional)

    def chat(self, message, stream=False, temperature=0.7, max_tokens=None):
        """
        Send a message to the model.
        :param message: User input text
        :param stream: If True, stream tokens in real-time
        :param temperature: Controls randomness
        :param max_tokens: Limit output length
        """
        url = f"{self.base_url}/v1/chat/completions"

        payload = {
            "model": self.model,
            "messages": self.history + [{"role": "user", "content": message}],
            "temperature": temperature,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens

        headers = {"Content-Type": "application/json"}

        if stream:
            return self._stream_request(url, payload, headers)
        else:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                reply = data["choices"][0]["message"]["content"]
                self.history.append({"role": "user", "content": message})
                self.history.append({"role": "assistant", "content": reply})
                return reply
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")

    def _stream_request(self, url, payload, headers):
        """
        Handle streaming output.
        """
        with requests.post(url, headers=headers, json=payload, stream=True) as response:
            if response.status_code != 200:
                raise Exception(f"Error {response.status_code}: {response.text}")

            print("\nAssistant:", end=" ", flush=True)
            full_text = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode("utf-8"))
                        delta = data.get("choices", [{}])[0].get("delta", {}).get("content")
                        if delta:
                            print(delta, end="", flush=True)
                            full_text += delta
                    except json.JSONDecodeError:
                        continue

            print("\n")
            self.history.append({"role": "assistant", "content": full_text})
            return full_text

    def clear_history(self):
        """Clear stored chat history."""
        self.history = []

    def set_model(self, model_name):
        """Change the model."""
        self.model = model_name
        print(f"✅ Model switched to: {model_name}")

    def get_embedding(self, text):
        url = f"{self.base_url}/v1/embeddings"
        payload = {"model": self.model, "input": text}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["data"][0]["embedding"]
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    
if __name__ == "__main__":
    # Example usage
    client = OllamaClient(base_url="http://192.168.0.160:11434", model="qwen2.5:7b")

    # Non-streaming (gets full output)
    print("\n🔹 Non-streaming example:")
    reply = client.chat("you are a ai agent that can assist users in finding products now tell me what you need", stream=False)
    print("Assistant:", reply)
