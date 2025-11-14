from flask import Flask
import os
app = Flask('keep_alive')
@app.route('/')
def index():
    return 'Mehrozkiyad Professional Bot is alive'

def run_keep_alive():
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port)
