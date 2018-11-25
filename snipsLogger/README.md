<img align="right" src="https://avatars0.githubusercontent.com/u/2564618?s=200&amp;v=4" width=96></br>
# SNIPS-Logger

Python script as a service to provides a log file of most important SNIPS mqtt topics.
Basically, this script subscribe to hotword, intent, tss and such SNIPS topics, like a background sam watch, to provides a log files of what happens.
This allow to check what's going on while using SNIPS.

## Install

On the main SNIPS unit (the server), run this:

```
cd ~
git clone https://github.com/KiboOst/SNIPS-Tips/snipsLogger
cd snipsLogger
sudo chmod +x install.sh
sudo ./install.sh
```
This will install the script as a service, so it runs in background.
By default, it will connect on localhost, port 1883. If you need to change this, you can stop the service, edit the python script, and start the service.
Also, by default, the script will keep only 200 lines in log file.

```
sudo systemctl stop snipslogger
sudo nano /home/pi/snipsLogger/snipsLogger.py
sudo systemctl start snipslogger
```

## Read log
snipsLogger will log to a simple text file so you can simply read it with:
```
cat /home/pi/snipsLogger/snipsLog.txt
```

Here is an example of log file:

```
25-11-2018 11:59:20 -- snipsLogger starting
25-11-2018 12:00:11 | ON_HOTWORD | SiteId: salle | modelId: heySnips_Kiboost
25-11-2018 12:00:12 | ON_LISTENING | SiteId: salle
25-11-2018 12:00:14 | ON_THINK | SiteId: salle | text: éteins la lumière
25-11-2018 12:00:16 | ON_SUCCESS | SiteId: None | intent: {u'intentName': u'kiboost:lightsTurnOffJeedom', u'probability': 1.0}
25-11-2018 12:00:17 | ON_SAY | SiteId: salle | text: ok.
```

## Uninstall
If you want to completely remove this script and service, do the following:

```
sudo systemctl disable snipslogger
sudo rm -rf snipsLogger
```

-----------------
#### 2018-11-25
- First public version.


## License

The MIT License (MIT)

Copyright (c) 2018 KiboOst

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

