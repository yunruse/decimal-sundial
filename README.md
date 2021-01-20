# sundial
## A remarkably witchy datetime formatter

`sundial` is a datetime formatter, albeit with a twist. In addition to regular Pythonic strftime symbols like `%H:%M:%S`, it lets you timekeep in your own way – by a sundial, or by decimal time (a la Revolutionary France).

In particular, if the current date was `2021-12-03 14:49`, its solar time would be `14:06:45` and its decimal time `6:17:36`.

- `*d`: day-of-month with decimals (`3.617`);
- `*e`: _solar_ day-of-month with decimals (`3.338`);
- `*h`: _solar_ hour (`14`)
- `*m`: _solar_ minute (`6`);
- `*s`: _solar_ second (`45`);
- `*a`: decimal hour, 0 to 10 (`6`);
- `*b`: decimal minute, 0 to 100 (`17`);
- `*c`: decimal second, 0 to 100 (`36`);

(In any of the above, using a capital letter adds relevant leading zeros. Trailing zeros are always included.)

In the above, _solar_ time is defined like a sundial: 6AM is sunrise and 6PM is sunset. (The solar decimal is where 0 is sunrise and 0.5 is sunset.) At the moment, it is defined rigidly in a way where 6PM to 6AM will likely have significantly differing units, especially if you get much more or much less than exactly 12 hours of sunlight.

At the current moment the project is in very early alpha; it was originally designed to be a menubar-only app. I intend to add a command-line interface ASAP, however.

Comes with macOS menubar app, which leverages `menubar.json` defined as:
    {
      "coords": [y, x],  # coordinates for accurate solar knowledge
      "menubar": fmtstring,  # format shown on menu
    }

Due to a limitation in the menubar library, the menubar cannot update every second; it would skip over two seconds every now and then. As such, it updates at a more CPU-respecting rate of 30 seconds.

![A menubar app saying "1.508 sol".](/screenshot.png)