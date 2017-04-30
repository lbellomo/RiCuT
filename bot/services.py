import requests
import json
from math import sin, cos, sqrt, atan2, radians
from key import keys
from urllib.request import urlopen

def get_wind_data(lat=35, lon=139):
    app_id = keys['owm']
    url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID={}"
    url = url.format(lat,lon, app_id) 
    r = requests.get(url)
    j = json.loads(r.text)
    return j.get('wind')['deg'],j.get['wind']['speed']


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

"""
def check_point_into_elipse(x, y, cx, cy, r1, r2):

    #dado el punto (x,y) verificar que esta dentro de la elipse con centro (cx,cy)
    #y radio mayor r1 y radio menor r2

    return (((x-cx)**2)/(r1**2))+(((y-cy)**2)/(r2**2))) <= 1
"""

"""
def elipse_foco(pos_x, pos_y, wind_deg, wind_speed):

    #generar parametros de una elipse alrededor de un foco
    #de incendio en (pos_x, pos_y) y parametros de vector de viento
    #degrees y velocidad

    return (pos_x, pos_y, wind_speed*math.cos(wind_deg), wind_speed*math.sin(wind_deg), wind_deg)
"""

def get_image(path):
    photo = urlopen("http://192.168.33.137:8000/map.png")
    return photo

def get_message(peligro, lat1, lon1, lat2, lon2, direc):
        
    dist = dist_fuego_persona(lat1, lon1, lat2, lon2)    
    msg = "usted esta en {} debe dirigirse a direccion {} para escapar"
    
    if peligro

        
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


