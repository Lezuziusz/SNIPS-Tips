


<img align="right" src="https://avatars0.githubusercontent.com/u/2564618?s=200&amp;v=4" width=96></br>
# SNIPS-Tips

#### This repository is for documenting some tips and tricks on SNIPS


## SNIPS with Jeedom
- Dynamic remapping of TTS : [JeedomTTSremap](JeedomTTSremap "JeedomTTSremap")</br>
Exp: Le volet du salon est {#[Salon][Volet][Etat]#|0:fermé|<99:ouvert à #[Salon][Volet][Etat]#|99:ouvert}
- SNIPS actions inside Jeedom : [JeedomSnipsActions](https://github.com/KiboOst/SNIPS-Tips/tree/master/JeedomSnipsActions)</br>
Trigger sam update-assistant, sam status, change tts volume, directly from Jeedom.

## SNIPS
- (:exclamation:New) [SNIPS logger](https://github.com/KiboOst/SNIPS-Tips/tree/master/snipsLogger) : Keep a log of what happens.
- [SNIPS Batch Tester](https://github.com/KiboOst/SNIPS-Tips/tree/master/pySnipsBatch) : Console batch sentences testing.
- More natural voice: equalize TTS! [snips_equal](https://github.com/KiboOst/SNIPS-Tips/tree/master/snips_equal)
- [SLC - Snips Led Control](https://github.com/Psychokiller1888/snipsLedControl) Control LEDs, with easy cutom animations or google/alexa animations. 
- SLC: [Mute hotword](https://github.com/KiboOst/SNIPS-Tips/tree/master/SLCcustom) with button.


## Ressources

- [SNIPS official website](https://snips.ai/)
- [SNIPS official Github](https://github.com/snipsco)
- [SNIPS Jeedom Doc](https://snips.gitbook.io/documentation/home-automation-platforms/jeedom-fr)
- [Awesome SNIPS](https://github.com/snipsco/awesome-snips)

## Some commands for everyday use

### sam
`sam status` | show status of connected device, services running etc.</br>
`sam watch` | see all mqtt messages (hotword detection, talking, intent catched etc.)</br>
`sam update-assistant` | update the assistant from console to your device.

### Divers
`dpkg -l | grep snips` | Display all snips components versions.</br>
`sudo systemctl restart snips-*` | restart all snips services.

### Others
`sudo apt-get update && sudo apt-get dist-upgrade` | Update all system and components.</br>
`snips-template render` | Render actions snippets to skills.</br>
`snips-skill-server -vvv` | Run snips-skill-server with verbose.</br>
`sudo systemctl stop snips-audio-server && snips-audio-server -vvv` | stop and run audio-server with verbose.</br>
`journalctl -u snips-audio-server.service` | Show audio-server service log.

## SNIPS folders

`/var/lib/snips/skills` : rendered skills from actions snippets codes.</br>
`/usr/share/snips/assistant` : assistant files, snippets, etc.</br>
`/etc/snips.toml` : SNIPS general configuration file (`sudo nano /etc/snips.toml`).
