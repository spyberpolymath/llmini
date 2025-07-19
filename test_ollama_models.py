import requests

# Ollama runs a local server at http://localhost:11434
OLLAMA_URL = "http://localhost:11434"

def list_models():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags")
        r.raise_for_status()
        models = r.json().get("models", [])
        print("Available Ollama models:")
        for m in models:
            print(f"- {m['name']}")
        return [m['name'] for m in models]
    except Exception as e:
        print("Could not connect to Ollama or list models:", e)
        return []

def test_model(model_name, prompt="What is the capital of France?"):
    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
        r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=60)
        r.raise_for_status()
        response = r.json()
        print(f"\nModel: {model_name}\nResponse: {response.get('response', '')[:300]}")
    except Exception as e:
        print(f"\nModel: {model_name}\nError: {e}")

if __name__ == "__main__":
    models = list_models()
    for model in models:
        test_model(model)
