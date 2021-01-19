import rumps

from solar import Sun

class Statusbar(rumps.App):    
    def __init__(self, lat, lon):
        self.sun = Sun(lat, lon)
        self.precision = 4
        rumps.App.__init__(self, self.time())
    
    def time(self):
        p = self.precision
        time = str(round(self.sun.sundial(), p)).zfill(p)
        return time + ' sol'    
    
    @rumps.clicked("3 digits")
    def precision(self, sender):
        sender.state = not sender.state
        self.precision = 3 if sender.state else 2

    @rumps.timer(0.01)
    def on_tick(self, sender):
        # add time to bottom of menu?
        self.title = self.time()

if __name__ == '__main__':
    # TODO: config file for app support
    LAT, LON = 55.7, -4.5
    self = Statusbar(LAT, LON)
    self.run()
