import requests
import configparser

# Load the parameters from the config file
config = configparser.ConfigParser()
config.read('Update Secret Password\\config.param')

vault_url = config.get('KEYVAULT', 'vault_url')
tenant_id = config.get('KEYVAULT', 'tenant_id')
client_id = config.get('KEYVAULT', 'client_id')
client_secret = config.get('KEYVAULT', 'client_secret')


# Set up the request URL and data to get an access token
url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "resource": "https://vault.azure.net"
}

# Send the request to get an access token
response = requests.post(url, data=data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract the access token from the response JSON
    access_token = response.json()["access_token"]
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")

# Set up the request headers with the access token
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Set up the request URL to get a list of secrets
url = f"{vault_url}/secrets?api-version=7.2"

# Send the request to the Azure Key Vault REST API
response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract the list of secrets from the response JSON
    secrets = response.json()["value"]
    print(secrets)
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")

for secret in secrets:
    secret_url = secret["id"]

    # Use HTTPS for requests
    azure_url = f'{secret_url}?api-version=7.3'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    azure_secret_response = requests.get(azure_url, headers=headers, verify=True)

    # Check the response status code
    if azure_secret_response.status_code == 200:
        # Successful request
        secret_value = azure_secret_response.json().get("value")
    else:
        # Error occurred
        print(f"Error: {azure_secret_response.status_code} - {azure_secret_response.text}")

    print(secret_value)

    # # Use the json parameter for POST requests
    # update_secret_url = f"{third_party_url}/ServerManage/UpdateSecret"
    # payload = {"SecretName": secret_name}
    # headers = {"accept": "*/*", "content-type": "application/json"}
    # response = requests.post(update_secret_url, json=payload, headers=headers, verify=True)

    # # Check the response status code
    # if response.status_code == 200:
    #     # Successful request
    #     print(response.json())
    # else:
    #     # Error occurred
    #     print(f"Error: {response.status_code} - {response.text}")
