import sys
import json
import urllib.request
import codecs

ARG_ON = 'on'
ARG_OFF = 'off'
ARG_STATE = 'state'
ARG_SET_BROKER = 'set_broker'
ARG_GET_BROKER = 'get_broker'

ARG_IP = sys.argv[1]
ARG_ACTION = sys.argv[2]

URL = "http://" + ARG_IP + "/xled/v1/"

LOGIN_URL = URL + "login"
VERIFY_URL = URL + "verify"
MODE_URL = URL + "led/mode"
MQTT_URL = URL + "mqtt/config"

AUTH_HEADER = 'X-Auth-Token'

AUTHENTICATION_TOKEN = 'authentication_token'
CHALLENGE_RESPONSE = 'challenge-response'
MODE = 'mode'
MODE_ON = 'movie'
MODE_OFF = 'off'

HEADERS = {'Content-Type': 'application/json'}
LOGIN_DATA = {'challenge': 'AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8='}
TURN_ON_DATA = {MODE: MODE_ON}
TURN_OFF_DATA = {MODE: MODE_OFF}

def formatData(data):
  return json.dumps(data).encode('utf8')

def processRequest(request):
  return urllib.request.urlopen(request)

def processRequestJSON(request):
  loginResponse = processRequest(request)
  reader = codecs.getreader("utf-8")
  return json.load(reader(loginResponse))

# login to api - get challenge response and auth token
loginRequest = urllib.request.Request(url = LOGIN_URL, headers = HEADERS, data = formatData(LOGIN_DATA))
loginData = processRequestJSON(loginRequest)

challengeResponse = loginData[CHALLENGE_RESPONSE]
authToken = loginData[AUTHENTICATION_TOKEN]

HEADERS[AUTH_HEADER] = authToken
verifyData = {CHALLENGE_RESPONSE: challengeResponse}

# verify token by responding with challenge response
verifyRequest = urllib.request.Request(url = VERIFY_URL, headers = HEADERS, data = formatData(verifyData))
verifyData = processRequestJSON(verifyRequest)

def turnOn():
  onRequest = urllib.request.Request(url = MODE_URL, headers = HEADERS, data = formatData(TURN_ON_DATA))
  processRequest(onRequest)
  print(1)

def turnOff():
  offRequest = urllib.request.Request(url = MODE_URL, headers = HEADERS, data = formatData(TURN_OFF_DATA))
  processRequest(offRequest)
  print(0)

def getState():
  modeRequest = urllib.request.Request(url = MODE_URL, headers = HEADERS)
  modeData = processRequestJSON(modeRequest)

  if modeData[MODE] != MODE_OFF:
    print(1)
  else:
    print(0)

def getBroker():
  request = urllib.request.Request(url = MQTT_URL, headers = HEADERS)
  print(processRequestJSON(request))

def setBroker(broker):
  payload = { 'broker_host': broker }
  request = urllib.request.Request(url = MQTT_URL, headers = HEADERS, data = formatData(payload))
  print(processRequestJSON(request))


if ARG_ACTION == ARG_ON:
  turnOn()
elif ARG_ACTION == ARG_OFF:
  turnOff()
elif ARG_ACTION == ARG_STATE:
  getState()
elif ARG_ACTION == ARG_GET_BROKER:
  getBroker()
elif ARG_ACTION == ARG_SET_BROKER:
  setBroker(sys.argv[3])
