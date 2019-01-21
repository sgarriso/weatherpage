# python default imports
import requests, json

# project related imports
import location
#setting up logging info
import log
log_handle=log.setup()

# this script uses an API powered by https://newsapi.org/
def get_key():
    log_handle.info("getting News API")
    return ''

# this is the default base url to help build the query to the news api    
def get_base_url():
    log_handle.info(" getting base url for news")
    return "https://newsapi.org/v2/top-headlines?country=us&"
def build_url_call(base_url=None,key=None):
    log_handle.info("Building url for news API")
    if not base_url:
        base_url = get_base_url()
    if not key:
        key = get_key()
    
    complete_url = base_url +  "apiKey=" + key
    return complete_url

#gets the news data
def get_data(complete_url=None):
    if not complete_url:
        complete_url = build_url_call()
    response = requests.get(complete_url)
    
    if response.ok:
        return response.json() 
    else:
        # TODO: handle the error
        response.raise_for_status()
def test():
    log_handle.info(get_data())

