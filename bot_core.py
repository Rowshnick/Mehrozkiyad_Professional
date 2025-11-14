import os
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from astro.core import compute_chart
from healing.mappings import select
from sigil.ai import generate as ai_generate
from sigil.local import generate_local
from utils.text_ai import generate_text
from models import SessionLocal, User, Broadcast, init_db
from datetime import datetime
LANG, NAME, GENDER, BDATE, BTIME, BPLACE, TARGET = range(7)
init_db()
def start(update, context):
    keyboard = [['فارسی','English']]
    update.message.reply_text('Please choose language / لطفاً زبان را انتخاب کنید:', reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return LANG
def lang_chosen(update, context):
    lang = update.message.text.strip().lower(); context.user_data['lang'] = 'fa' if 'فار' in lang else 'en'
    msg = 'خوش آمدید! لطفاً نام کوچک را وارد کنید.' if context.user_data['lang']=='fa' else 'Welcome! Please enter your first name.'
    update.message.reply_text(msg); return NAME
def name_h(update, context): context.user_data['name']=update.message.text.strip(); update.message.reply_text('جنسیت یا skip' if context.user_data['lang']=='fa' else 'Gender or skip'); return GENDER
def gender_h(update, context): context.user_data['gender']=update.message.text.strip(); update.message.reply_text('تاریخ تولد YYYY-MM-DD' if context.user_data['lang']=='fa' else 'Birth date YYYY-MM-DD'); return BDATE
def bdate_h(update, context):
    txt=update.message.text.strip()
    try:
        dt=datetime.strptime(txt,'%Y-%m-%d')
        context.user_data['birth_date']=dt
        update.message.reply_text('ساعت تولد HH:MM یا skip' if context.user_data['lang']=='fa' else 'Birth time HH:MM or skip')
        return BTIME
    except:
        update.message.reply_text('فرمت اشتباه' if context.user_data['lang']=='fa' else 'Invalid format')
        return BDATE
def btime_h(update, context):
    txt=update.message.text.strip()
    if txt.lower()=='skip': context.user_data['birth_time']=None
    else:
        try: context.user_data['birth_time']=datetime.strptime(txt,'%H:%M')
        except: update.message.reply_text('فرمت اشتباه' if context.user_data['lang']=='fa' else 'Invalid time'); return BTIME
    update.message.reply_text('شهر تولد یا skip' if context.user_data['lang']=='fa' else 'Birth place or skip'); return BPLACE
def bplace_h(update, context): txt=update.message.text.strip(); context.user_data['birth_place']=None if txt.lower()=='skip' else txt; update.message.reply_text('هدف: wealth / love / health / career' if context.user_data['lang']=='fa' else 'Goal: wealth / love / health / career'); return TARGET
def target_h(update, context):
    goal=update.message.text.strip().lower(); context.user_data['goal']=goal
    bd=context.user_data.get('birth_date'); bt=context.user_data.get('birth_time')
    if bt: birth_dt=datetime(bd.year,bd.month,bd.day,bt.hour,bt.minute)
    else: birth_dt=datetime(bd.year,bd.month,bd.day,12,0)
    chart=compute_chart(birth_dt,0); sel=select(goal); summary=generate_text(context.user_data.get('name'), goal, chart)
    zodiac=chart.get('sun'); prompt=f"A mythic cosmic sigil for {context.user_data.get('name')} in the style of Mehrozkiyad: zodiac {zodiac}, theme {goal}, ornate golden frame, high detail"
    ai_file=ai_generate(prompt, f"outputs/sigils/{context.user_data.get('name')}_ai.png")
    if ai_file is None: ai_file=generate_local(context.user_data.get('name'), zodiac)
    db=SessionLocal(); tg_user=update.message.from_user; user=db.query(User).filter(User.tg_id==tg_user.id).first()
    if not user:
        user=User(tg_id=tg_user.id, name=context.user_data.get('name'), lang=context.user_data.get('lang'), gender=context.user_data.get('gender'), birth_date=str(context.user_data.get('birth_date')))
        db.add(user); db.commit()
    if context.user_data['lang']=='fa':
        fa_text=f"نتیجه برای {context.user_data.get('name')}\nخورشید: {zodiac}\nسنگ‌ها: {', '.join([s['fa'] for s in sel['stones']])}\nگیاهان: {', '.join([h['fa'] for h in sel['herbs']])}\n\n{summary.get('fa')}"
        update.message.reply_text(fa_text); update.message.reply_photo(open(ai_file,'rb'))
    else:
        en_text=f"Result for {context.user_data.get('name')}\nSun: {zodiac}\nStones: {', '.join([s['en'] for s in sel['stones']])}\nHerbs: {', '.join([h['en'] for h in sel['herbs']])}\n\n{summary.get('en')}"
        update.message.reply_text(en_text); update.message.reply_photo(open(ai_file,'rb'))
    db.close(); return ConversationHandler.END
def cancel(update, context): update.message.reply_text('لغو' if context.user_data.get('lang')=='fa' else 'Cancelled'); return ConversationHandler.END
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

def run():
    token=os.environ.get('TG_BOT_TOKEN')
    if not token:
        print('TG_BOT_TOKEN not set in environment')
        return
    updater=Updater(token, use_context=True); dp=updater.dispatcher
    conv=ConversationHandler(entry_points=[CommandHandler('start', start)], states={LANG:[MessageHandler(Filters.text & ~Filters.command, lang_chosen)], NAME:[MessageHandler(Filters.text & ~Filters.command, name_h)], GENDER:[MessageHandler(Filters.text & ~Filters.command, gender_h)], BDATE:[MessageHandler(Filters.text & ~Filters.command, bdate_h)], BTIME:[MessageHandler(Filters.text & ~Filters.command, btime_h)], BPLACE:[MessageHandler(Filters.text & ~Filters.command, bplace_h)], TARGET:[MessageHandler(Filters.text & ~Filters.command, target_h)]}, fallbacks=[CommandHandler('cancel', cancel)])
    dp.add_handler(conv)
    print('Bot polling started')
    updater.start_polling(); updater.idle()
