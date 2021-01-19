from datetime import datetime, timedelta

import requests

URL = 'https://api.sunrise-sunset.org/json'
DATE = '%y-%m-%d '
TIME = '%H:%M:%S'

def date(string):
    PM = string.endswith('PM')
    if PM or string.endswith('AM'):
        string = string[:-3]
    today = datetime.now().strftime(DATE)
    date = datetime.strptime(today + string, DATE+TIME)
    if PM:
        date += timedelta(hours=12)
    return date

class Sun:
    def __init__(self, lat, lon):
        self.params = {'lat': lat, 'lng': lon, 'formatted': 1}
        self.refresh()

    def refresh(self):
        data = requests.get(URL, params=self.params).json()['results']
        self.sunrise = date(data['sunrise'])
        self.sunset = date(data['sunset'])

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


    def sundial(self, date=None):
        # TODO: check and refresh every ~12 hours
        date = date or datetime.now()
        return (date - self.sunrise) / (self.sunset - self.sunrise)
