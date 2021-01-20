__version__ = '0.1'

from datetime import datetime, timedelta
import json
import os

import rumps

from solar import Sun, DAY

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
        rumps.App.__init__(self, '')
        self.on_tick(None)

    def load(self, conf):
        self.conf = conf
        self.sun = Sun(*conf['coords'])
        self.last_event = None

    @rumps.timer(4)
    def on_tick(self, sender):
        # add time to bottom of menu?
        self.title = self.sun.strftime(self.conf.get('menubar'))

    def next_event(self, index=1):
        name, date = self.sun.events()[index]
        return Event(name, date)

    @rumps.timer(60 * 60)
    def refresh_data(self):
        self.sun.refresh()

    @rumps.clicked("Sundial")
    def config(self, sender):
        if rumps.alert(
            f'sundial --menubar (v{__version__})',
            'Developed with love by Mia yun Ruse <3',
            'Project on GitHub...', 'OK'
        ):
            import webbrowser
            webbrowser.open_new_tab(
                "https://github.com/yunruse/decimal-sundial")


if __name__ == '__main__':
    with open('config.json') as f:
        self = Statusbar(json.load(f))
    self.run()
