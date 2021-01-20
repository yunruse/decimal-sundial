__version__ = '0.1'

from datetime import datetime, timedelta
import json
import os

import rumps

from solar import Sun

class Event:
    def __init__(self, tag, date):
        self.tag = tag
        self.date = date

        n = tag.replace('_', ' ')
        if 'twilight' in n:
            n = n.replace('begin', 'start') + 's'
        self.name = n

    def msg(self):
        minutes = (self.date - datetime.now()).seconds // 60
        h, m = divmod(minutes, 60)
        return f'In {h}h {m}m, {self.name}'


class Statusbar(rumps.App):
    def __init__(self, conf):
        self.load(conf)
        rumps.App.__init__(self, self.time())

    def load(self, conf):
        self.conf = conf
        self.sun = Sun(*conf['coords'])
        self.last_event = None

    def time(self, fmt=None, date=None):
        date = date or datetime.now()
        fmt = fmt or "*d sol"
        p = self.conf.get('precision', 3)

        h, m, s, ms = self.sun.as_clock(date)

        fmt = date.strftime(fmt)
        for a, b in (
            ('*d', str(round(self.sun.sundial(), p)).zfill(p)),
            ('*h', str(int(h)).zfill(2)),
            ('*m', str(int(m)).zfill(2)),
            ('*s', str(int(s)).zfill(2)),
            ('*.', str(round(ms, 3)).replace('0.', '')),
            ('**', '*'),
        ):
            fmt = fmt.replace(a, b)
        return fmt

    @rumps.timer(0.01)
    def on_tick(self, sender):
        # add time to bottom of menu?
        self.title = self.time(fmt=conf.get('menubar'))

    def next_event(self, index=1):
        name, date = self.sun.events()[index]
        return Event(name, date)
        
    @rumps.timer(3)
    def eventy(self, s):
        try:
            self.eventloop(s)
        except Exception as e:
            print(e)
    
    def eventloop(self, sender):
        if not self.conf.get('event_notif', False):
            return
        event = self.next_event()
        
        # handle notification and menubar-setting logic
        if self.last_event == event.tag:
            return
        self.last_event = event.tag
        
        event2 = self.next_event(2)
        self.menu = [
            rumps.MenuItem(event.msg()),
            rumps.MenuItem(event2.msg()),
        ]

    @rumps.timer(60 * 60)
    def refresh_data(self):
        self.sun.refresh()

    @rumps.clicked("Configure...")
    def config(self, sender):
        f = __file__.replace('menubar.py', 'config.json')
        print(f)
        os.system(f'open {f}')

    @rumps.clicked("About...")
    def config(self, sender):
        if rumps.alert(
            f'Decimal Sundial v{__version__}',
            'Developed with love by Mia yun Ruse',
            'Project on GitHub...', 'OK'
        ):
            import webbrowser
            webbrowser.open_new_tab(
                "https://github.com/yunruse/decimal-sundial")


if __name__ == '__main__':
    with open('config.json') as f:
        conf = json.load(f)
    self = Statusbar(conf)
    self.run()
