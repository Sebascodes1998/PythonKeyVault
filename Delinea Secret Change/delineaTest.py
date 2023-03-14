import http.client
import urllib
import json
import requests
import configparser

# Load the parameters from the config file
config = configparser.ConfigParser()
config.read('config.param')

delinea_site = config.get('KEYVAULT', 'delinea_site')
token = config.get('KEYVAULT', 'token')
secret_to_change = config.get('KEYVAULT', 'secret_to_change')

delinea_site = '[Your Secret Server Site]' #ex: http://domain.com/SecretServer
authApi = '/oauth2/token'
api = delinea_site + '/api/v1'

def UpdateSecret(token, secret):        
    headers = {'Authorization':'Bearer ' + token, 'content-type':'application/json'}
    secretId = secret['id']
    resp = requests.put(api + '/secrets/' + str(secretId), json=secret, headers=headers)    
    
    if resp.status_code not in (200, 304):
        raise Exception("Error updating Secret. %s %s" % (resp.status_code, resp))    
    return resp.json()

#REST call to retrieve a secret by ID
def GetSecret(token, secretId):
    headers = {'Authorization':'Bearer ' + token, 'content-type':'application/json'}
    resp = requests.get(api + '/secrets/' + str(secretId), headers=headers)    
    
    if resp.status_code not in (200, 304):
        raise Exception("Error retrieving Secret. %s %s" % (resp.status_code, resp))    
    return resp.json()

#Retrieves the secret item by its "slug" value
def GetItemBySlug(secretItems, slug):
    for x in secret['items']:
        if x['slug'] == slug:
            return x
    raise Exception('Item not found for slug: %s' % slug)

#Updates the secret item on the secret with the updated secret item
def UpdateSecretItem(secret, updatedItem):
    secretItems = secret['items']
    for x in secretItems:
        if x['itemId'] == updatedItem['itemId']:
            x.update(updatedItem)
            return
    raise Exception('Secret item not found for item id: %s' % str(updatedItem['itemId']))

secret = GetSecret(token, secret_to_change)
print("Secret Name: " + secret['name'])
print("Secret ID: " + str(secret['id']))
print("Active: " + str(secret['active']))
print(secret)