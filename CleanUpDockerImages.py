import json
import requests

baseurl='https://mylabserver.com/artifactory/'
repoListUrl=baseurl+'api/repositories?type=LOCAL'
url = baseurl+'api/search/aql'
username='admin'
password='password'
stableVersionCount=3

# Functions
def processRepo(repoName):
    response=getRequest(baseurl+'api/docker/'+repoName+'/v2/_catalog',username,password)
    if(response.status_code==200):
            registryList=json.loads(response.text)
            for r in registryList['repositories']:
                print "##### Search images in "+r+" registry #####"
                searchRegistry(r)

def searchRegistry(registry):
    payload='items.find({"@isProd":{"$eq":"yes"},"@docker.repoName":{"$eq":"'+registry+'"},"property.key":{"$eq":"docker.repoName"}}).include("created","modified","path","repo","name","updated","id").sort({"$desc": ["created"]}).limit('+str(stableVersionCount)+')'
    response=postRequest(url,payload,username,password)
    imageList=json.loads(response.text)
    if(len(imageList['results']) >= stableVersionCount):
            stableImage=imageList['results'][stableVersionCount-1]
            createdDate=stableImage['created']
            print '!!!!! All images will be deleted older than '+stableImage["repo"]+'/'+stableImage["path"]+' !!!!!'
            payload='items.find({"@DND": {"$ne":"yes"},"created": {"$lt":"'+createdDate+'"},"@docker.repoName":{"$eq":"'+registry+'"},"property.key":{"$eq":"docker.repoName"}})'
            response=postRequest(url,payload,username,password)
            imageDeletionList=json.loads(response.text)
            for r in imageDeletionList['results']:
                deleteurl=baseurl+r['repo']+'/'+r['path']
                print '----- Deleting Image '+deleteurl+' -----'
                deleteRequest(deleteurl,username,password)

def getRequest(url,username,password):
    return requests.get(url,auth=(username,password), verify=False)

def postRequest(url,payload,username,password):
    return requests.post(url,data=payload, auth=(username,password), verify=False)

def deleteRequest(url,username,password):
    return requests.delete(url,auth=(username,password), verify=False)

# Cleanup
jsonString = getRequest(repoListUrl,username,password)
r=json.loads(jsonString.text)
repoList=['test-local','docker-dev-local2']
for result in r:
  if result['key'] in repoList:
        print "**** Iterate "+result['key']+" repo and print the images that can be deleted. ****"
        processRepo(result['key'])