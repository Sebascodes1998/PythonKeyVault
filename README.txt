README.txt

This script is used to retrieve secrets from an Azure Key Vault using Azure AD authentication.

Before running this script, ensure that you have replaced the following values with your own actual values:

tenant_id
client_id
client_secret
vault_url
third_party_url (if applicable)
This script uses the Requests library to send HTTP requests to the Azure Key Vault REST API. It first requests an access token using the client credentials flow, then uses the access token to authenticate subsequent requests to retrieve secrets.

To use this script, run it in a Python environment that has the Requests library installed. The script will print out the values of all secrets found in the specified Azure Key Vault.

Note that this script is for demonstration purposes only and should be used with caution in production environments.