"""
https://developers.facebook.com/docs/pages/access-tokens
To make data collection scripts working we should get long-live page access token.
It's a bit confusing...

Before all we need to create application in https://developers.facebook.com/
"""

import requests

# # # # # Input parameters

APP_ID = 00000000000000 #settings -> basic
APP_SECRET = 'soMestringWiTHlettersANDnumbers' #ettings -> basic
SHORT_LIVED_TOKEN = 'loooooooongSTringWiTHlettersANDnumbers' #tools -> explorer

# # # # #

# To get a long-lived User access token
resp = requests.get(f"https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={SHORT_LIVED_TOKEN}")

resp.json()
# {'access_token': 'VeryVERYloooooooongSTringWiTHlettersANDnumbers',
#  'token_type': 'bearer'}

LONG_LIVED_USER_ACCESS_TOKEN = resp.json()['access_token']

# get personal user ID
user_resp = requests.get(f"https://graph.facebook.com/me?fields=id,name&access_token={LONG_LIVED_USER_ACCESS_TOKEN}")
user_resp.json()
# {'id': '000000000000000000', 'name': 'Your Name'}

USER_ID = user_resp.json()['id']

# get page access token
resp_page = requests.get(f"https://graph.facebook.com/{USER_ID}/accounts?fields=name,access_token&access_token={LONG_LIVED_USER_ACCESS_TOKEN}")

resp_page.json()

# {'data': [{'name': 'GroupName',
#    'access_token': 'VeryVERYloooooooongSTringWiTHlettersANDnumbers',
#    'id': '28908000000000000118117'}],
#  'paging': {'cursors': {'before': 'azazazazaza',
#    'after': 'azazazaza'}}}

DB_LONG_LIVED_TOKEN = resp_page.json()['data'][0]['access_token']
# this one is exactly what we need! now store it in env(PATH) and use wisely!

