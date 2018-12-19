import requests
import json

jenkinsUrl='https://jenkins.com'
username='admin'
password='password'

def getRequest(url,username,password):
    return requests.get(url,auth=(username,password), verify=False)

def postRequest(url,payload,username,password):
    return requests.post(url,data=payload, auth=(username,password), verify=False)


# Get list of slaves from Jenkins

url=jenkinsUrl+'/computer/api/json'
jsonString = getRequest(url,username,password)
r=json.loads(jsonString.text)
for result in r['computer']:
	if(result['displayName'] != 'master' and result['offline']):
		reconnectUrl=jenkinsUrl+'/computer/'+result['displayName']+'/launchSlaveAgent'
		print 'Restarting Agent '+result['displayName']+' using api '+reconnectUrl+' ...'
		response=postRequest(reconnectUrl,username,password)
