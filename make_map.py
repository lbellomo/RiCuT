import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
from mpl_toolkits.basemap import Basemap

def make_map(lon_e=-32.08, lat_e=-64.53, width_e=0.01, height_e=0.02,
             angle_e=30, lon_p=-32.083, lat_p=-64.532):
    '''
    Crea un mapa centrado en la lon_p, lat_p, y dibuja la elipse.
    lon_e: lon elipse (float)
    lat_e: lat elipse (float)
    width_e: width elipse (float)
    height_e: height elipse (float)
    angle_e: angle elipse (float)
    lon_p: lon persona (float)
    '''
    plt.figure(figsize=(12,12))

    # Encontramos las esquinas del mapa, centrado en la persona. 
    
    m = Basemap(llcrnrlon=lat_p - 0.05,llcrnrlat=lon_p - 0.05 ,
                urcrnrlon=lat_p + 0.05,urcrnrlat=lon_p + 0.05, epsg=4221)

    #http://server.arcgisonline.com/arcgis/rest/services
    # One can use two kinds of streetmaps: ESRI_Imagery_World_2D or World_Street_Map

    m.arcgisimage(service='World_Street_Map', xpixels = 500, verbose= True)


    #x, y = m(lat,lon)
    e = Ellipse(xy=[lat_e,lon_e], width=width_e, height=height_e, angle=angle_e)
    e.set_alpha(0.3)
    ax = plt.gca()
    ax.add_artist(e)

    m.scatter(lat_p, lon_p, marker='o',alpha=0.5,color='r',s=100)

    # Si no existe la carpeta la creamos.
    if not os.path.isdir('maps'):
        os.mkdir('maps')
    
    # Creamos el nombre en funcion de la pos de la persona
    file_name = "map_" + str(lon_p) + "_" + str(lat_p) + ".png"
    plt.savefig("maps/" + file_name)
    return file_name