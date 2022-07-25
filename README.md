# Zerodha Login Automated - Selenium Based; Supported by Lambda function that processes the redirect rul and stores accessk key to DynamoDB

## Context
This code is for a python package for automated login to Zerodha. The redirect URL is not handled here - Separate Repo with a container that runs as a lambda function saves the access token to dynamoDB

## How to productionalize
- Get Zerodha (kite.trade) account for API based access to the platform.
- Create a '.zerodha' file in your home directory (Sample provided - check .zerodha.sample file)
    - Needed Variables in File are Zerodha API keys/secret and login credentials (Userid, Password, PIN)
    - One additional variable defined - ZAPI_AUTH: This can be any string that you choose. This string gets added as a query parameter in Zerodha reddirect response. The redirect response handler can test this 'api_auth' query parameter to ensure the response is from zerodha and is in response to call from this package

    The url for logging in being used is - f'https://kite.trade/connect/login?v=3&api_key={api_key}&redirect_params={quote_plus(f"api_auth={api_auth}")}' which sends the ZAPI_AUTH parameter as redirect query parameter 'api_auth'
- Set up a dynamodb table "save_access" with partition key as 'date' (string variable) and sort key as 'datetime' (also a string)
- Check out the zerodha-dynamodb-save-accesstoken repository to set up a lambda function to handle Zerodha redirect url (it saves the access token in the save_access table in dynamodb)
- Install zlogin package from pypi, "pip install zlogin"

```python
import zlogin
access_token = zlogin.fetch_access_token()
```

    When logging in - send this as a redirect parameter 'api_auth'. For this, your Zerodha login URL will be
    f'https://kite.trade/connect/login?v=3&api_key={api_key}&redirect_params={quote_plus(f"api_auth={api_auth}")}'

## This repo is a sister repo with zerodha-dynamodb-save-accesstoken tool which has a container code for lambda function that handles storage of access token to dynamodb; 
That tool creates the redirect to the API gateway. For both to work properly, please use the same  ZAPI_AUTH environment variable value in both places
