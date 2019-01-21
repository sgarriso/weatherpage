# python default imports
import requests, json

# project related imports
import location
#setting up logging info
import log
log_handle=log.setup()


#25e989bd41e3e24ce13173d8126e0fd6
# this is the default key if no key is given. this key was given to me by FreightWise, LLC
def get_key():
    log_handle.info("getting weather API")
    return '25e989bd41e3e24ce13173d8126e0fd6'

# this is the default base url to help build the query to the weather api    
def get_base_url(word="weather"):
    log_handle.info(" getting base url for %s" %(word))
                 
    return "http://api.openweathermap.org/data/2.5/%s?" %(word)
                 
def build_url_call(base_url,city,key):
    complete_url = base_url +  "appid=" + key + "&q=" + city
    return complete_url

# if no city or key is given. the default key will be used. the city default will call the location api which will use your ip to guess your local area. (given to me from FreightWise, LLC)
def get_current_weather(city=None,key=None):
    log_handle.info(" getting current weather data")
    if not city:
        city=location.get_location_by_ip()
    if not key:
        key = get_key()
        
    return get_data(build_url_call(get_base_url(),city,key))

def get_map_url(lat,lng,zoom=10,layer='precipitation',key=None):
    url = 'https://openweathermap.org/weathermap?basemap=map&cities=true&layer=%s&lat=%s&lon=%s&zoom=%s' % (layer,lat,lng,zoom)
    return url
        
        
def get_forecast(city=None,key=None):
                 
    #http://api.openweathermap.org/data/2.5/forecast?q=London,us&mode=json&appid=25e989bd41e3e24ce13173d8126e0fd6
    if not city:
        city=location.get_location_by_ip()
    if not key:
        key = get_key()
        return get_data(build_url_call(get_base_url('forecast'),city,key))
                 
def get_coord(data):
    coord = data['coord']
    return coord['lon'],coord['lat']
def get_data(complete_url):
    response = requests.get(complete_url)
    
    if response.ok:
        return response.json() 
    else:
        # TODO: handle the error
        response.raise_for_status()
# unit test cases
def test_all():
    city=location.get_location()
    get_weather = get_current_weather(city=city)
    forecast = get_forecast(city=city)
    y,x = get_coord(get_weather)
    


    
