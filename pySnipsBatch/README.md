# SNIPS Batch Tester

The SNIPS console allow sentence testing, but only one by one, display intent and slot.
Here is a python script that allow to test a batch of sentences in one go, each with the intent it should match !
Why this tool ? Actually, the SNIPS NLU is quiet limited. For example, you can have a sentence matching the right intent, retrain your assistant with exact same configuration, and same sentence doesn't match anymore. This is due to several limitations in the NLU:

- SNIPS NLU is bag of word type, so no semantic is taken into account.
- Not all training sentences are taken each time for performance reason, which insert random behavior.
- It do words simplification, two words which are almost the same can be seen as the same by the NLU.

So, each time I change something in slots or intent training sentences, I had to try a lot of sentences one by one with copy/paste to be sure not all was over. Here came the idea of batch testing sentences in one go.

Basically, this python script will connect to SNIPS console with your credentials, and send request with sentence to test, just like you do by hand on the console. It will then read and parse the result and display it.
Here is a result example:

> [Intent MATCHED] "éteins la lumière de la cuisine" | intentName: kiboost:lightsTurnOffJeedom | 0.69531906
slotName: house_room | entity: house_room | rawValue: cuisine | value: cuisine

> [!!Intent UNMATCHED!!] "maman aura quel age dans deux ans et demi" | intentName: kiboost:getAge | 0.50317174
slotName: forename | entity: forename | rawValue: maman | value: aurelie
slotName: age | entity: snips/number | rawValue: deux | value: 2

Here is the batch.json file corresponding to test these two sentences:
```json
{
	"éteins la lumière de la cuisine": "kiboost:lightsTurnOffJeedom ",
	"maman aura quel age dans deux ans et demi": "kiboost:getNextAge"
}
```
### How to

- Download files batch.json and pySnipsBatcher.py in same folder.
- Edit batch.json with your sentences and intent name it should match (or let '').
- Edit pySnipsBatcher.py to put your SNIPS console credentials into ```if __name__ == "__main__":```

```
You can find your project ID (proj_xxxx) in your url when connected on your console assistant. Ex: https://console.snips.ai/assistants/proj_xxxx
```

You can either enter sentences directly in the script:

```python
if __name__ == "__main__":
	#snips console credentials and project:
	login = "myloginemail"
	password = "mysnipspass"
	project = "proj_xxxxxx"

	#connect to your console:
	snips = snipsBatcher(login, password, project)

	#test single sentence on console:
	result = snips.testQuery("ouvre les volets")

	#display result with intent that should matches:
	snips.showResult(result, 'kiboost:OpenCoverJeedom')
```

Or use the batch.json file:
```python
if __name__ == "__main__":
	#snips console credentials and project:
	login = "myloginemail"
	password = "mysnipspass"
	project = "proj_xxxxxx"

	#connect to your console:
	snips = snipsBatcher(login, password, project)

	#load batch.json file to test:
	batchJson = json.load(open('batch.json', 'rb'), encoding='utf-8')

	for item in batchJson:
		if _debug: debug(3, 'batch test: %s | %s'%(item, batchJson[item]))
		result = snips.testQuery(item)
		snips.showResult(result, batchJson[item])
```

You can also specify snips.showResult(result, batchJson[item], True) to show only unmatched results if any.

Then, just run pySnipsBatcher.py file and read output :wink:

Here is a 46 test sentences result:
```
[13:36:39:Starting \_Dev\snips\BatchTesting\pySnipsBatcher.py...]
matched: 46 | unmatched: 0 | total: 46
[Finished in 62.0s]
```

1 min waiting against 46 copy/paste :stuck_out_tongue_winking_eye:

-----------------
#### 2018-11-01
- First public version.

## License

The MIT License (MIT)

Copyright (c) 2018 KiboOst

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

