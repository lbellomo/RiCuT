import requests
import json
from math import sin, cos, sqrt, atan2, radians
from key import keys
from urllib.request import urlopen

"""
from make_map import make_map
from ellipse import ellipse
"""

def get_wind_data(lat=35, lon=139):
    app_id = keys['owm']
    url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID={}"
    url = url.format(lat,lon, app_id) 
    r = requests.get(url)
    j = json.loads(r.text)
    return j.get['wind']['speed'],j.get('wind')['deg']


def get_modis():
    """
        'latitude,longitude,brightness,scan,track,acq_date,acq_time,satellite,confidence,version,bright_t31,frp,daynight'
    """

    r = requests.get('https://firms.modaps.eosdis.nasa.gov/active_fire/c6/text/MODIS_C6_South_America_24h.csv')
    data = r.text
    data = data.split('\n')
    data.pop(0) #eliminamos cabeceras
    data.pop()  #eliminamos dato vacio
    pares = [float((e.split(',')[0]), float(e.split(',')[1])) for e in d] #armamos pares
    return [pares[0]]

def get_image(path="file:///home/pbovina/space/RiCuT/bot/maps/{}", name='map.png'):
    photo = urlopen(path.format(name))
    return name, photo

def get_message(peligro=True, lat1=10.22, lon1=10.22, lat2=15.22, lon2=15.22, direc="norte"):
        
    dist = dist_fuego_persona(lat1, lon1, lat2, lon2)    
    msg = "Usted esta en {} debe dirigirse a direccion {} para escapar"
    
    if peligro:
        return msg.format("peligro", direc)
    
    msg1 = "Usted esta a salvo respecto a la zona de peligro a una distancia de {}"
    return msg1.format(dist)

def get_message_distance(peligro=True, lat1=10.22, lon1=10.22, lat2=15.22, lon2=15.22, direc="norte"):

    dist = dist_fuego_persona(lat1, lon1, lat2, lon2) 
    msg1 = "Usted esta a salvo respecto a la zona de peligro a una distancia de {}"
    return msg1.format(dist)

"""
def respuesta(pp_lat,pp_lon):
    fuego = get_modis()[0] # par de lat lon del fuego
    viento = get_wind_data(fuego[0], fuego[1]) # obtenemos viendo en centro del fuego
    #return (ce_lat, ce_long, ps_lat, ps_long, a, b, alfa)
    el = ellipse(fuego[0], fuego[1], pp_lat, pp_lon, viento[0], viento[1])
    #(lon_e=-32.08, lat_e=-64.53, width_e=0.01, height_e=0.02,angle_e=30, lon_p=-32.085, lat_p=-64.53, lon_s=-32.083, lat_s=-64.532):    
    name = make_map(el[0], el[1], el[4], el[5], el[6], el[2], el[3], pp_lon, pp_lat, ):   
    
    if el[2] == None or el[3] == None:        
        orien = direccion_flecha(pp_lat,pp_lon,el[2],el[3]))
        msg = get_message(False,pp_lat,pp_lon,fuego[0],fuego[1], orien)
        photo = get_photo(name)
        return msg, photo

    orien = direccion_flecha(pp_lat,pp_lon,el[2],el[3]))
    msg = get_message(False,pp_lat,pp_lon,fuego[0],fuego[1], orien)
    photo = get_photo(name)
    return msg, photo  
"""

def dist_fuego_persona(lat1, lon1, lat2, lon2):

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def direccion_flecha(lat1=1, lon=1, lat2=1, lon2=1):
    return "norte"