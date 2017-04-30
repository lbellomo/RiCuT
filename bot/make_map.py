def make_map(lon_e=-32.08, lat_e=-64.53, width_e=0.01, height_e=0.02,
             angle_e=30, lon_p=-32.085, lat_p=-64.53, lon_s=-32.083, lat_s=-64.532):
    '''
    Crea una imagen centrada en la persona, dibuja la zona de peligro y la salida.
    
    Parameters:
    -----------
    lon_e: lon elipse (float)
    lat_e: lat elipse (float)
    width_e: width elipse (float)
    height_e: height elipse (float)
    angle_e: angle elipse (float)
    lon_p: lon persona (float)
    lat_p: lat persona (float)
    lon_s: lon salida (float)
    lat_s: lat salida (float)
    
    Return:
    -------
    file_name: nombre del archivo
    '''
    plt.figure(figsize=(12,12))

    # Encontramos las esquinas del mapa, centrado en la persona. 
    
    m = Basemap(llcrnrlon=lat_p - 0.05,llcrnrlat=lon_p - 0.05 ,
                urcrnrlon=lat_p + 0.05,urcrnrlat=lon_p + 0.05, epsg=4221)

    #http://server.arcgisonline.com/arcgis/rest/services
    # One can use two kinds of streetmaps: ESRI_Imagery_World_2D or World_Street_Map

    m.arcgisimage(service='World_Street_Map', xpixels = 500, ypixels=500, verbose= True)


    #x, y = m(lat,lon)
    e = Ellipse(xy=[lat_e,lon_e], width=width_e, height=height_e, angle=angle_e)
    e.set_alpha(0.3)
    ax = plt.gca()
    ax.add_artist(e)

    # Agregamos a la persona
    m.scatter(lat_p, lon_p, marker='o',alpha=0.5,color='k',s=100)

    # Agregamos el fuego
    #m.scatter(lat_f, lon_f, marker='o', alpha=0.7, color='r', s=200)
    
    dx = lat_p - lat_s
    dy = lon_p - lon_s
    
    # Agregamos la flecha de la direccion de salida.
    ax.arrow(lat_p, lon_p, dx, dy, head_width=0.002, head_length=0.002, fc='k', ec='k')

    # Si no existe la carpeta la creamos.
    if not os.path.isdir('maps'):
        os.mkdir('maps')
    
    # Creamos el nombre en funcion de la pos de la persona
    file_name = "map_" + str(lon_p) + "_" + str(lat_p) + ".png"
    plt.savefig("maps/" + file_name)
    
    return file_name
