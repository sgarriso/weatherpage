import geocoder
import log
log_handle=log.setup()
def get_location():
    log_handle.info("testing location")
    return "Brentwood,Tennessee"
def get_location_by_ip(ip=None):
    
    log_handle.info("testing ip")
    if not ip:
        g = geocoder.ip('me')
    else:
        g = geocoder.ip(ip)
    return g.city + "," + g.state

def test():
    get_location_by_ip()
