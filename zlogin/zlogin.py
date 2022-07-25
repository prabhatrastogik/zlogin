"""
ZLOGIN Module is for auto-login for Zerodha and storage of the access token to dynamoDB. 
This works in conjunction with store_access module which creates a Lambda container handling re-direct url from zerodha
"""
import os
import sys
from time import sleep
from urllib.parse import quote_plus
from datetime import datetime

from logging import getLogger, INFO

import boto3
from undetected_chromedriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

logger = getLogger("Zlogin")
logger.setLevel(INFO)


def add_env_vars_from_file():
    path = os.path.expanduser('~/.zerodha')
    with open(path, 'r') as f:
        env_vars = dict(tuple(line.replace('\n', '').split('=')) for line
                        in f.readlines() if not line.startswith('#'))
    os.environ.update(env_vars)


def get_env_vars():
    add_env_vars_from_file()
    all_keys = dict(
        api_key=os.getenv('ZAPI'),
        api_secret=os.getenv('ZSECRET'),
        api_auth=os.getenv('ZAPI_AUTH'),
        user_id=os.getenv('ZUSER'),
        pw=os.getenv('ZPASS'),
        twofa_key=os.getenv('ZTFA'),
    )
    return all_keys


def get_driver():
    options = ChromeOptions()
    options.headless = True
    logger.info("Driver Options Created")
    driver = Chrome(options=options)
    logger.info("Chrome Created")
    return driver


def generate_request_token(api_key, user_id, pw, twofa_key, api_auth, **kwargs):
    logger.info("Generate Function Started")
    driver = get_driver()
    logger.info("Driver Acquired")
    driver.get(
        f'https://kite.trade/connect/login?v=3&api_key={api_key}&redirect_params={quote_plus(f"api_auth={api_auth}")}')
    login_id = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(By.XPATH, '//*[@id="userid"]'))
    login_id.send_keys(user_id)
    logger.info("USER ID Sent")
    pwd = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(By.XPATH, '//*[@id="password"]'))
    pwd.send_keys(pw)
    logger.info("Pw Sent")
    sleep(1)
    submit = WebDriverWait(driver, 10).until(lambda x: x.find_element(
        By.XPATH, '//*[@id="container"]/div/div/div[2]/form/div[4]/button'))
    submit.click()
    logger.info("Login Btn Clicked")
    totp = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(By.XPATH, '//*[@id="pin"]'))
    totp.send_keys(twofa_key)
    logger.info("TFA Sent")
    sleep(2)
    continue_btn = WebDriverWait(driver, 10).until(lambda x: x.find_element(
        By.XPATH, '//*[@id="container"]/div/div/div[2]/form/div[3]/button'))
    continue_btn.click()
    logger.info("Request Token Generated!")


def fetch_access_token():
    """
    This function fetches access token either from Dynamodb - if the token exists for today - or generates request_token
    and passes to the Lambda function to get access_token and save to DynamoDB
    Args: 
        None
    Requirements: 
        A '.zerodha' file in the home directory with values for ZAPI, ZSECRET, ZAPI_AUTH, ZUSER, ZPASS, ZTFA
        Sample in the repo
    """
    dynamodb = boto3.resource('dynamodb')
    access_store = dynamodb.Table('access_store')
    today = datetime.utcnow().date().strftime('%Y-%m-%d')
    date_rows = access_store.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key(
            'date').eq(today),
        ScanIndexForward=False
    )['Items']
    if not date_rows:
        logger.info("Access token for today does not exist - Generating new..")
        generate_request_token(**get_env_vars())
        wait_seconds = 0
        while not date_rows:
            date_rows = access_store.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key(
                    'date').eq(today),
                ScanIndexForward=False
            )['Items']
            sleep(1)
            wait_seconds += 1
            logger.info(f'Seconds Waited: {wait_seconds}')
            if wait_seconds > 10:
                logger.info(
                    f'Exiting without success in reading newly generated access token - Seconds Waited: {wait_seconds}')
                break
    try:
        logger.info("Access Token Returned!")
        return date_rows[0]['access_token']
    except Exception as e:
        logger.error(
            'Access token not generated - Neither does one exist for today')
        raise e


if __name__ == "__main__":
    print(fetch_access_token())
