from datetime import datetime, timedelta
import json

import requests

URL = 'https://api.sunrise-sunset.org/json'
DATE = '%y-%m-%d '
TIME = '%H:%M:%S'
DAY = timedelta(hours=24)

def date(string):
    PM = string.endswith('PM')
    if PM or string.endswith('AM'):
        string = string[:-3]
    today = datetime.now().strftime(DATE)
    date = datetime.strptime(today + string, DATE+TIME)
    if PM:
        date += DAY / 2
    return date

class Sun:
    def __init__(self, lat, lon):
        self.params = {'lat': lat, 'lng': lon, 'formatted': 1}
        self.refresh()

    def refresh(self):
        self.data = requests.get(URL, params=self.params).json()['results']
        self.sunrise = date(self.data['sunrise'])
        self.sunset = date(self.data['sunset'])

    def events(self, now=None):
        now = now or datetime.now()
        def offset(date):
            if date < now:
                date += DAY
            return date

        # todo: get events in the correct day rather than extrapolate
        noon = self.sunrise + (self.sunset - self.sunrise) / 2
        midnight = self.sunset + (self.sunrise + DAY - self.sunset) / 2
        events = [
            ('now', now),
            ('sunrise', self.sunrise),
            ('noon', noon),
            ('sunset', self.sunset),
            ('midnight', midnight)
        ]
        
        events += [
            (k, offset(date(d)))
            for k, d in self.data.items()
            if 'twilight' in k]
        events.sort(key=lambda q: q[1])
        
        return events

    def sundial(self, date=None, fix_night=False):
        '''
        Return decimal time, where 0 is sunrise and 1 is sunset.

        If fix_night, 2 is sunset. Otherwise, it's free to vary
        proportionally to the length of the day.
        '''
        
        solar_day = (self.sunset - self.sunrise)
        solar_night = (self.sunrise + DAY - self.sunset)
        day = DAY / solar_day
        date = date or datetime.now()
        
        dial = (date - self.sunrise) / solar_day
        
        if fix_night:
            if date > self.sunset:
                dial = 1 + (date - self.sunset) / solar_night
            if date < self.sunrise:
                dial = 2 - (self.sunrise - date) / solar_night
        return dial % day

    def as_clock(self, date=None):
        t = self.sundial(date, True)
        h = ((t * 12) + 6) % 24
        h, m = divmod(h * 60, 60)
        m, s = divmod(m * 60, 60)
        s, ms = divmod(s, 1)
        return int(h), int(m), int(s), int(ms * 1000)

    def strftime(self, string, date=None):
        date = date or datetime.now()
        
        h, m, s, ms = self.as_clock(date)
        sundial = self.sundial(date, True) / 2
        day_start = date.replace(hour=0, minute=0, second=0)
        
        solar = date.day + sundial / 2
        decimal = (date - day_start) / DAY
        a = decimal * 10
        a, b = divmod(a, 1)
        b, c = divmod(b * 100, 1)
        c *= 100

        string = date.strftime(string)
        # TODO: process symbols char-by-char
        CLOCK = ['1d', '02d']
        CALDAY = [f'.3f', f'06.3f']
        for sym, val, fmts in (
            ('d', date.day + decimal, CALDAY),
            ('e', date.day + sundial, CALDAY),
            ('h', h, CLOCK),
            ('m', m, CLOCK),
            ('s', s, CLOCK),
            ('a', a, ['1d', '1d']),
            ('b', b, CLOCK),
            ('c', c, CLOCK),
        ):
            for with_zero in (False, True):
                if with_zero:
                    sym = sym.upper()
                fmt = fmts[with_zero]
                if fmt.endswith('d'):
                    val = int(val)
                string = string.replace('*'+sym, format(val, fmt))
        return string
        
def _show_events(sun):
    day = DAY / (self.sunset - self.sunrise)
    for name, date in self.events():
        hhmm = date.strftime('%H:%M')
        sol = sun.sundial(date)
        if name == 'sunrise':
            sol = day
        if sol > day:
            continue
        print(f'{name:27} {sol:+.3f} ({hhmm})'.replace('+', ' '))

def test_time(sun, date):
    print(date)
    letters = 'dehmsabc'
    for i in letters:
        print(i, self.strftime('*'+i, date))

if __name__ == '__main__':
    with open('config.json') as f:
        conf = json.load(f)
    
    self = Sun(*conf['coords'])
    test_time(self, datetime(2020, 12, 3, 14, 49))
