import os, base64
try:
    import openai
except Exception:
    openai = None

def generate(prompt, filename):
    if openai is None or os.getenv('OPENAI_API_KEY') is None:
        return None
    openai.api_key = os.getenv('OPENAI_API_KEY')
    try:
        resp = openai.Image.create(prompt=prompt, n=1, size='1024x1024')
        data = resp['data'][0]
        b64 = data.get('b64_json') or data.get('b64')
        img_bytes = base64.b64decode(b64)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename,'wb') as f: f.write(img_bytes)
        return filename
    except Exception as e:
        print('AI image generation failed:', e)
        return None
