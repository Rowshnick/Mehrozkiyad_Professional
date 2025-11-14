import os
try:
    import openai
except Exception:
    openai = None

def generate_text(name, goal, chart):
    en = f"Short advisory for {name} about {goal}. Sun: {chart.get('sun')}, Moon: {chart.get('moon')}"
    fa = f"توصیه‌ای کوتاه برای {name} دربارهٔ {goal}. خورشید: {chart.get('sun')}, ماه: {chart.get('moon')}"
    if openai and os.getenv('OPENAI_API_KEY'):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        try:
            r_en = openai.Completion.create(engine='text-davinci-003', prompt=en, max_tokens=200)
            r_fa = openai.Completion.create(engine='text-davinci-003', prompt=fa, max_tokens=200)
            return {'en': r_en.choices[0].text.strip(), 'fa': r_fa.choices[0].text.strip()}
        except Exception as e:
            print('OpenAI call failed:', e)
    return {'en': en, 'fa': fa}
