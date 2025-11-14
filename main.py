import os, threading
from keep_alive import run_keep_alive
from admin_app import app as admin_app
from models import init_db
init_db()
# start keep alive
threading.Thread(target=run_keep_alive, daemon=True).start()
# admin UI
threading.Thread(target=lambda: admin_app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000))+1), daemon=True).start()
# ask for tokens
if not os.environ.get('TG_BOT_TOKEN'):
    try:
        os.environ['TG_BOT_TOKEN']=input('Enter your TELEGRAM BOT TOKEN: ').strip()
    except:
        pass
if not os.environ.get('ADMIN_PASSWORD'):
    try:
        os.environ['ADMIN_PASSWORD']=input('Set ADMIN PASSWORD: ').strip()
    except:
        pass
# run bot
from bot_core import run
print('Starting bot...')
run()
