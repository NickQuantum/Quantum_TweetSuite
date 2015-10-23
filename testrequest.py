# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 05:22:38 2015

@author: srini_000
"""

import requests
from requests_oauthlib import OAuth1

payload ={'id':'654538555360997376'}

## add oauth
##headers = {'consumer_key':'5zvyqirbbnbPxUX67ixXBwQ5G','consumer_secret':'8iGil6zWJvK7qjGj0z7xguSvaiIbZtpH0Z3UumAVetv88e9xbX','access_token':'2995170696-z5tNgtrnhR5zc5tT4sB6knKBTrCKHehOljhs1l2','access_token_secret':'wOcuYhfpvwxFZ6TmNvyPb9fPpEnH1fvfApiEZFnFGUuJk'}
auth = OAuth1('5zvyqirbbnbPxUX67ixXBwQ5G','8iGil6zWJvK7qjGj0z7xguSvaiIbZtpH0Z3UumAVetv88e9xbX','2995170696-z5tNgtrnhR5zc5tT4sB6knKBTrCKHehOljhs1l2','wOcuYhfpvwxFZ6TmNvyPb9fPpEnH1fvfApiEZFnFGUuJk')
r = requests.get('https://api.twitter.com/1.1/statuses/oembed.json?maxwidth=250&hide_media=1&hide_thread=1&omit_script=1&align=left',params =payload,auth =auth)

print (r.url)

htmlcontent = r.json()

print htmlcontent['html']
