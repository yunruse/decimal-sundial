from datetime import datetime, timedelta

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
        twilights = [('now', now)]
        
        def offset(date):
            return date if date > now else date + DAY
        
        twilights += [
            (k, offset(date(d)))
            for k, d in self.data.items()
            if 'twilight' in k]        
        twilights.sort(key=lambda q: q[1])
        return twilights

    def sundial(self, date=None, fix_night=False):
        '''
        Return decimal time, where 0 is sunrise and 1 is sunset.

        If fix_night, 2 is sunset. Otherwise, it's free to vary
        proportionally to the length of the day.
        '''
        # TODO: check and refresh every ~12 hours
        date = date or datetime.now()
        dial = (date - self.sunrise) / (self.sunset - self.sunrise)
        if fix_night and dial > 1:
            dial = 1 + (date - self.sunset) / (self.sunrise + DAY - self.sunset)
        return dial

    def as_clock(self, date=None):
        t = self.sundial(date, True)
        h = (t * 12) + 6
        h, m = divmod(h * 60, 60)
        m, s = divmod(m * 60, 60)
        s, ms = divmod(s, 1)
        return h, m, s, ms
