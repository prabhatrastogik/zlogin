# Zerodha Login Automated; This package reads access token stored in dynamodb and provides KiteConnect / KiteTicker instances.
# This package can only be used in conjunction with a dynamodb access_store that keeps access key stored 
## Context
This code is for a python package for automated login to Zerodha. The redirect URL is not handled here - Separate Repos with a container that runs as a lambda function saves the access token to dynamoDB

Check out zlogin-puppeteer (headless chrome based login to zerodha) [can be hosted for free in Google cloud functions]
and zerodha-dynamodb-save-accesstoken [AWS lambda container] to save access token to dynamodb from redirect url.

## How to productionalize
- Get Zerodha (kite.trade) account for API based access to the platform.
- Save the API key as env variable ZAPI

- Checkout zlogin-puppeteer repository that automates login process (using headless chrome)
- Check out the zerodha-dynamodb-save-accesstoken repository to set up a lambda function to handle Zerodha redirect url (it saves the access token in the save_access table in dynamodb)
- Install zlogin package from pypi, "pip install zlogin"

```python
import zlogin
access_token = zlogin.fetch_access_token()
```

## This repo is a sister repo with zerodha-dynamodb-save-accesstoken & zlogin-puppeteer tools which have a container code for lambda function that handles storage of access token to dynamodb and puppeteer based Google Cloud Function code to handle login process which redirects to the lambda.
