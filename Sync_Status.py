import json
import requests
import sys

baseurl='http://192.168.33.10:8081/artifactory/'
repoListUrl=baseurl+'api/repositories?type=LOCAL'
username='admin'
password='password'

# Functions
def getRequest(url,username,password):
    return requests.get(url,auth=(username,password), verify=False)

# Get Status
jsonString = getRequest(repoListUrl,username,password)
r=json.loads(jsonString.text)
errorflag='false'
status=['never_run','error','inconsistent']
for result in r:
  jsonResponse=getRequest(baseurl+'api/replication/'+result['key'],username,password)
  replicationStatus=json.loads(jsonResponse.text)
  if(replicationStatus['status'] in status): 
    print 'Replication failed in repository '+result['key'] + ' : Status - "' + replicationStatus['status'] + '"'
    errorflag='true'
# Check for Errors 
if(errorflag=='true'):
    sys.exit("Replication Failed")