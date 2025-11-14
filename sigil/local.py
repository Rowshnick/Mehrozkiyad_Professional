from PIL import Image, ImageDraw, ImageFont
import os
SYMS={'Aries':'♈','Taurus':'♉','Gemini':'♊','Cancer':'♋','Leo':'♌','Virgo':'♍','Libra':'♎','Scorpio':'♏','Sagittarius':'♐','Capricorn':'♑','Aquarius':'♒','Pisces':'♓'}
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def generate_local(name,zodiac,out_path=None):
    size=(1024,1024); img=Image.new('RGB',size,(18,24,44)); draw=ImageDraw.Draw(img)
    sym=SYMS.get(zodiac,'?')
    try:
        f=ImageFont.truetype(FONT,240); w,h=draw.textsize(sym,font=f); draw.text(((size[0]-w)/2,200), sym, font=f, fill=(245,220,130))
    except:
        draw.text((size[0]//2-50,200), sym, fill=(245,220,130))
    try:
        f2=ImageFont.truetype(FONT,36); w,h=draw.textsize(name,font=f2); draw.text(((size[0]-w)/2,880), name, font=f2, fill=(230,230,230))
    except:
        draw.text((size[0]//2-100,880), name, fill=(230,230,230))
    if out_path is None: out_path=f'outputs/sigils/{name}_{zodiac}.png'
    os.makedirs(os.path.dirname(out_path), exist_ok=True); img.save(out_path)
    return out_path
