
## Snips Led Control : Mute hotword button

[SLC - Snips Led Control](https://github.com/Psychokiller1888/snipsLedControl) is an amazing tool for controling LEDs with SNIPS.

It provides a nice custom leds pattern by default, and here is how to mute hotword detection with the Respeaker 2 Mic Pi HAT button. It can be adapted to any Pi HAT with button anyway.

Edit custom pattern file:
```
sudo nano /snipsLedControl/ledPatterns/CustomLedPattern.py
```
This file define what SLC will does when triggering function like listening, wakeup on hotword detection, speaking, etc.

At the top, import call function from subprocess module:
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.LedPattern import LedPattern
import time
import threading
from subprocess import call
```
In *init* function we will ad a new variable that will store the muted state:

```python
class CustomLedPattern(LedPattern):
	def __init__(self, controller):
		super(CustomLedPattern, self).__init__(controller)
		self._animation = threading.Event()
		self.muted = False
```

Then, we will change the *onButton1* and *idle* function.
Here, I change the idle function so, instead of breathing the three leds (on Respeaker 2 mic), when muted it will breath only the center led to reflect its state.

The *onButton1* function will check muted state and stop or start hotword service, then restart *idle* function so it reflects the new state.

```python
	def idle(self, *args):
		self.off()
		self._animation.set()
		if self.muted:
			middleLed = int(self._numLeds/2)
			while self._animation.isSet():
				self.breathLeds(1, [0, 0, 75], [middleLed])
		else:
			while self._animation.isSet():
				self.breathLeds(1, [0, 0, 75])

	def onButton1(self, *args):
		#mute hotword detection:
		self._animation.clear()
		self.off()
		if self.muted:
			self.muted = False
			call('sudo systemctl start snips-hotword.service', shell=True)
		else:
			self.muted = True
			call('sudo systemctl stop snips-hotword.service', shell=True)
		self._controller.idle()
```

So here you are. In muted state, you can use SNIPS to send TTS command (to speak to you) like usual, but you can't speak to it.

Just save your CustomLedPattern and restart SLC.

You can find the complete CustomLedPattern.py file here also.

Need to turn LEDs on or off at night with Jeedom ? Check [here](https://github.com/KiboOst/SNIPS-Tips/tree/master/JeedomSnipsActions)

--------------

## License

The MIT License (MIT)

Copyright (c) 2018 KiboOst

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
