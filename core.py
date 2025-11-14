import swisseph as swe
from datetime import datetime, timezone, timedelta
SIGNS=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
PLANETS={'Sun':swe.SUN,'Moon':swe.MOON}

def compute_chart(birth_dt_local, tz_offset_hours=0):
    if birth_dt_local.tzinfo is None:
        utc = birth_dt_local - timedelta(hours=tz_offset_hours)
        utc = utc.replace(tzinfo=timezone.utc)
    else:
        utc = birth_dt_local.astimezone(timezone.utc)
    jd = swe.julday(utc.year, utc.month, utc.day, utc.hour + utc.minute/60.0)
    planets = {n: float(swe.calc_ut(jd,p)[0]%360) for n,p in PLANETS.items()}
    def sign_of(deg): return SIGNS[int(deg//30)%12]
    return {'sun': sign_of(planets['Sun']), 'moon': sign_of(planets['Moon']), 'planets':planets}
