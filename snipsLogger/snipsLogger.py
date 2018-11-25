#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys,os
import time
import datetime

import paho.mqtt.client as mqtt
import json

try:
	reload(sys)
	sys.setdefaultencoding('utf-8')
except:
	pass

_mqttSERVER_ = 'localhost'
_mqttPORT_ = 1883
_mqttTOPICS_ = {
				'ON_HOTWORD': 'hermes/hotword/default/detected',
				'ON_LISTENING': 'hermes/asr/startListening',
				'ON_THINK': 'hermes/asr/textCaptured',
				'ON_ERROR': 'hermes/nlu/intentNotRecognized',
				'ON_SUCCESS': 'hermes/nlu/intentParsed',
				'ON_SAY': 'hermes/tts/say',
				'ON_PLAY_FINISHED': 'hermes/audioServer/{}/playFinished',
				#'ON_TTS_FINISHED': 'hermes/tts/sayFinished',
				#'ON_HOTWORD_TOGGLE_ON': 'hermes/hotword/toggleOn',
				#'ON_HOTWORD_TOGGLE_OFF': 'hermes/hotword/toggleOff'
			}

_logKeepLines_ = 200
_logPath_ = os.path.dirname(os.path.abspath(__file__)) + '/snipsLog.txt'

_debug = False


class SnipsLogger(object):
	def __init__(self):
		self._mqttServer = _mqttSERVER_
		self._mqttPort = _mqttPORT_
		self.topics = _mqttTOPICS_
		self.dateTimeFormat = "%d-%m-%Y %H:%M:%S"

		self.addLog(datetime.datetime.now().strftime(self.dateTimeFormat) + ' -- snipsLogger starting')

		self._mqttClient = self.connectMqtt()
	#

	def connectMqtt(self):
		try:
			mqttClient = mqtt.Client()
			mqttClient.on_connect = self.onConnect
			mqttClient.on_message = self.onMessage
			mqttClient.connect(self._mqttServer, int(self._mqttPort))
			mqttClient.loop_start()
			return mqttClient
		except Exception as e:
			if _debug: debug(1, "connectMqtt ERROR: %s"%e)
			self.onStop()
	#

	def onConnect(self, client, userdata, flags, rc):
		for topic in _mqttTOPICS_:
			self._mqttClient.subscribe(_mqttTOPICS_[topic])
	#

	def onMessage(self, client, userdata, message):
		if _debug: debug(2, "onMessage topic: %s"%message.topic)

		payload = None
		siteId = None
		modelId = None

		text = None
		intent = None

		if hasattr(message, 'payload') and message.payload != '':
			payload = json.loads(message.payload)
			if _debug: debug(4, "onMessage payload: %s"%payload)

		if payload is not None:
			if 'siteId' in payload: siteId = payload['siteId']
			if 'modelId' in payload: modelId = payload['modelId']
			if 'text' in payload: text = payload['text']
			if 'intent' in payload: intent = payload['intent']

		toLog = datetime.datetime.now().strftime(self.dateTimeFormat)
		toLog += ' | '

		if message.topic == _mqttTOPICS_['ON_HOTWORD']:
			toLog += "%s | SiteId: %s | modelId: %s"%('ON_HOTWORD', siteId, modelId)

		if message.topic == _mqttTOPICS_['ON_LISTENING']:
			toLog += "%s | SiteId: %s"%('ON_LISTENING', siteId)

		if message.topic == _mqttTOPICS_['ON_THINK']:
			toLog += "%s | SiteId: %s | text: %s"%('ON_THINK', siteId, text)

		if message.topic == _mqttTOPICS_['ON_ERROR']:
			toLog += "%s | SiteId: %s"%('ON_ERROR', siteId)

		if message.topic == _mqttTOPICS_['ON_SUCCESS']:
			toLog += "%s | SiteId: %s | intent: %s"%('ON_SUCCESS', siteId, intent)

		if message.topic == _mqttTOPICS_['ON_SAY']:
			toLog += "%s | SiteId: %s | text: %s"%('ON_SAY', siteId, text)

		if message.topic == _mqttTOPICS_['ON_PLAY_FINISHED']:
			toLog += "%s | SiteId: %s"%('ON_PLAY_FINISHED', siteId)

		"""
		if message.topic == _mqttTOPICS_['ON_HOTWORD_TOGGLE_ON']:
			toLog += "%s | SiteId: %s"%('ON_HOTWORD_TOGGLE_ON', siteId)

		if message.topic == _mqttTOPICS_['ON_HOTWORD_TOGGLE_OFF']:
			toLog += "%s | SiteId: %s"%('ON_HOTWORD_TOGGLE_OFF', siteId)

		if message.topic == _mqttTOPICS_['ON_TTS_FINISHED']:
			toLog += "%s | SiteId: %s"%('ON_TTS_FINISHED', siteId)
		"""


		if _debug: debug(2, "onMessage: toLog %s"%toLog)
		self.addLog(toLog)
	#

	def addLog(self, logText=''):
		if os.path.isfile(_logPath_):
			content = open(_logPath_, 'r').read()
		else:
			content = ''

		num_lines = len(content.split('\n'))
		if num_lines > _logKeepLines_:
			lines = content.split('\n')
			lines = lines[-int(_logKeepLines_):]
			keepContent = ''
			for line in lines:
				keepContent += '\n' + line
			content = keepContent

		towrite = content + '\n' + logText
		open(_logPath_, 'w').write(towrite)
	#

	def onStop(self):
		if _debug: debug(1, "onStop")
		self.addLog(datetime.datetime.now().strftime(self.dateTimeFormat) + ' -- snipsLogger stopping')

		try:
			if self._mqttClient is not None:
				self._mqttClient.disconnect()
		except:
			pass

		RUNNING = False
		sys.exit(0)
	#
#

def debug(level, text):
	if _debug >= level:
		print("--debug:", text)
#



if __name__ == "__main__":
	snipsLog = SnipsLogger()

	RUNNING = True
	try:
		while RUNNING:
			time.sleep(0.1)
	except KeyboardInterrupt:
		pass

	snipsLog.onStop()
