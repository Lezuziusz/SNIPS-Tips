#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys, os

import json
import urllib

import urllib.request
requestUrl = urllib.request
parseUrl = urllib.parse
from http.cookiejar import CookieJar, LWPCookieJar

try:
	reload(sys)
	sys.setdefaultencoding('utf-8')
except:
	pass

_debug = False
#_debug = 3

class snipsBatcher():

	def testQuery(self, inputQuery):
		jsonObj = {
					"operationName": "NluInferenceQuery",
					"variables": {
						"assistantId": self._proj,
						"query": inputQuery
					},
					"query": "query NluInferenceQuery($assistantId: ID!, $query: String!) {\n  nluInference(assistantId: $assistantId, query: $query) {\n    input\n    status\n    intent {\n      intentName\n      probability\n      __typename\n    }\n    slots {\n      rawValue\n      value\n      range {\n        start\n        end\n        __typename\n      }\n      entity\n      slotName\n      __typename\n    }\n    __typename\n  }\n}\n"
				}

		jsonString = json.dumps(jsonObj)
		jsonString = '[' + jsonString + ']'
		answer = self.request('POST', self._urlHost, '/gql', jsonString)
		if _debug: debug(3, "testQuery:answer %s"%answer)
		return answer[0]['data']['nluInference']
	#

	def showResult(self, nluInference, matchIntent='', showOnlyUnmatched=False):
		self.tested += 1
		displayResult = ''
		showThis = True

		intentInput = nluInference['input']

		#no intent found:
		if not 'intentName' in nluInference['intent']:
			displayResult = '[!!No intent found!!] %s'%intentInput
			self.unmatched += 1
			if matchIntent != '':
				displayResult += ' should match: %s'%matchIntent
			print(displayResult)
			return False

		intentName = nluInference['intent']['intentName']
		intentProba = nluInference['intent']['probability']
		slots = nluInference['slots']

		if matchIntent != '':
			if matchIntent == intentName:
				if showOnlyUnmatched:
					showThis = False
				self.matched += 1
				displayResult += '[Intent MATCHED]'
			else:
				self.unmatched += 1
				displayResult += '[!!Intent UNMATCHED!!]'



		displayResult += ' "%s" | intentName: %s | %s'%(intentInput, intentName, intentProba)

		if showThis:
			print(displayResult)
			for slot in slots:
				slotName = slot['slotName']
				entity = slot['entity']
				rawValue = slot['rawValue']
				try:
					value = json.loads(slot['value'])['value']
				except:
					value = slot['value']
				displaySlotResult = 'slotName: %s | entity: %s | rawValue: %s | value: %s'%(slotName, entity, rawValue, value)
				print(displaySlotResult)
			if len(slots) == 0:
				print('No slot found')
			print()
	#

	def request(self, method, host, path='', jsonString=None, postinfo=None): #standard function handling all get/post request
		if self._reqHdl == None:
			self._reqHdl = requestUrl.build_opener(requestUrl.HTTPCookieProcessor(self.cookieJar))
			self._reqHdl.addheaders = [
						('User-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0'),
						('Connection', 'keep-alive'),
						('Referer', self._urlHost+'/login'),
						('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
						('Upgrade-Insecure-Requests', 1)
					]

		url = host+path
		if _debug: debug(4, 'request: %s method: %s postinfo: %s'%(url, method, postinfo))

		if method == 'GET':
			answer = self._reqHdl.open(url, timeout = 5)
		else:
			if jsonString != None:
				jsonBytes = jsonString.encode()
				req = urllib.request.Request(url, data=jsonBytes, headers={'Content-Type': 'application/json'})
				answer = self._reqHdl.open(req)

			if postinfo != None:
				data = parseUrl.urlencode(postinfo)
				if sys.version_info[0] == 3: data = data.encode()
				answer = self._reqHdl.open(url, data, timeout = 5)

		self.cookieJar.save(self._cookFile, ignore_discard=True)

		if jsonString != None:
			if _debug: debug(5, 'request info: %s'%answer.info())
			result = json.load(answer)
			return result

		return answer.read()
	#

	def connect(self):
		postinfo = {'email': self._login, 'password': self._password}
		answer = self.request('POST', self._urlHost, '/api/login', None, postinfo)
		if _debug: debug(4, 'answer connect: %s'%answer)
		if b'Wake word' in answer:
			return True
		return False
	#

	def __init__(self, login='', password='', project=''):
		self._version = 0.12
		self._login = login
		self._password = password
		self._proj = project

		self._urlHost = 'https://console.snips.ai'
		self._reqHdl = None
		self.cookieJar = LWPCookieJar()
		self._cookFile = ''

		self.matched = 0
		self.unmatched = 0
		self.tested = 0

		if os.access('/', os.W_OK):
			APIfolder = os.path.dirname(os.path.realpath(__file__))
			self._cookFile = APIfolder+'/snipsBatcher_cookies.txt'

		if self.connect() == True:
			if _debug: debug(1, "__SNIPS console connected__")
	#


def debug(level, text):
	if _debug >= level:
		print("--debug:", text)
#


#testing purpose:
if __name__ == "__main__":
	#snips console credentials and project:
	login = "myloginemail"
	password = "mysnipspass"
	project = "proj_xxxxxx"

	#connect to your console:
	snips = snipsBatcher(login, password, project)

	"""
	#test single sentence on console:
	result = snips.testQuery("ouvre les volets")

	#display result with intent that should matches:
	snips.showResult(result, 'kiboost:OpenCoverJeedom')
	"""

	#load batch.json file to test:
	batchJson = json.load(open('batch.json', 'rb'), encoding='utf-8')

	for item in batchJson:
		if _debug: debug(3, 'batch test: %s | %s'%(item, batchJson[item]))
		result = snips.testQuery(item)
		snips.showResult(result, batchJson[item])
		
	print('matched: %s | unmatched: %s | total: %s'%(snips.matched, snips.unmatched, snips.tested))
