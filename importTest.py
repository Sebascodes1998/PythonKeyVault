import requests

third_party_url = ''

# Replace with your actual Azure AD tenant ID, client ID, and client secret
tenant_id = "6962c7e8-a9a5-4fc7-9af6-5a52fa48da1c"
client_id = "27f490fb-81b1-4db7-b1d2-820b072fa3e8"
client_secret = "wSF8Q~YoCIO73MD0wqqVv3FCMEa-1UOLpjtGOcH0"

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



# Replace with your actual key vault URL
vault_url = "https://sebascodes1998-vault.vault.azure.net"

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

