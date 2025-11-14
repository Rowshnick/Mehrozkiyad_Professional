STONES={'Sun':[{'en':'Citrine','fa':'سیترین'}],'Moon':[{'en':'Moonstone','fa':'ماه‌سنگ'}],'Venus':[{'en':'Rose Quartz','fa':'کوارتز رز'}],'Mars':[{'en':'Red Jasper','fa':'جاسپر قرمز'}],'Jupiter':[{'en':'Amethyst','fa':'آمتیست'}],'Saturn':[{'en':'Hematite','fa':'هماتیت'}],'Mercury':[{'en':'Agate','fa':'عقیق'}]}
HERBS={'Sun':[{'en':'Saffron','fa':'زعفران'}],'Moon':[{'en':'Jasmine','fa':'یاس'}],'Venus':[{'en':'Rose','fa':'گل رز'}],'Mars':[{'en':'Ginger','fa':'زنجبیل'}],'Jupiter':[{'en':'Nutmeg','fa':'جوز هندی'}],'Saturn':[{'en':'Cedar','fa':'سدر'}],'Mercury':[{'en':'Mint','fa':'نعناع'}]}
GOAL_MAP={'wealth':'Jupiter','love':'Venus','health':'Mars','career':'Saturn'}

def select(goal):
    planet=GOAL_MAP.get(goal,'Venus')
    return {'planet':planet,'stones':STONES.get(planet,STONES['Sun']),'herbs':HERBS.get(planet,HERBS['Sun'])}
