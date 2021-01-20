# sundial
## A remarkably witchy datetime formatter

`sundial` is a datetime formatter, albeit with a twist. In addition to regular Pythonic strftime symbols like `%H:%M:%S`, it has its own for almost anything you'd want to record when it comes to time. In particular, if the current date was `2021-12-03 14:49`:

- `*d`: day-of-month with decimals, leading zero (`03.617`);
- `*e`: day-of-month with decimals (`3.617`);
- `*D`: _solar_ day-of-month with decimals (`03.338`) with leading zero;
- `*E`: _solar_ day-of-month with decimals (`3.338`);
- `*H`: _solar_ hour (`14`)
- `*M`: _solar_ minute (`06`);
- `*S`: _solar_ second (`45`);

In the above, _solar_ time is defined like a sundial: 6AM is sunrise and 6PM is sunset. (The solar decimal is where 0 is sunrise and 0.5 is sunset.) At the moment, it is defined rigidly in a way where 6PM to 6AM will likely have significantly differing units, especially if you get much more or much less than exactly 12 hours of sunlight.

At the current moment the project is in very early alpha; it was originally designed to be a menubar-only app. I intend to add a command-line interface ASAP, however.

Comes with macOS menubar app, which leverages `menubar.json` defined as:
    {
      "coords": [y, x],  # coordinates for accurate solar knowledge
      "menubar": fmtstring,  # format shown on menu
    }

![A menubar app saying "1.508 sol".](/screenshot.png)