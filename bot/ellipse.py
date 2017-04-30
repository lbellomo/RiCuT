import numpy as np
from matplotlib import pyplot

import pyproj


def ellipse(fi_lat, fi_long,pp_lat, pp_long, vel_modulo, vel_angulo, coef_A=3000.7428, coef_B=-3.9333):
    '''
    Return:
    -------
    ce_lat: latitud centro de la elipse
    ce_long: longitud centro de la elipse
    ps_lat: latitud del punto de salida
    ps_long: longitud del punto de salida
    a, b: eje mayor y menor de la elipse
    alfa: angulo de la elipse
    '''

    p = pyproj.Proj(init='epsg:3857')

    # mapeo x-y con long-lat
    #fi_x = fi_long # antes de usar pyproj
    #fi_y =  fi_lat # antes de usar pyproj
    fi_x, fi_y = p(fi_lat, fi_long)

    #pp_x = pp_long # antes de usar pyproj
    #pp_y = pp_lat  # antes de usar pyproj
    pp_x, pp_y = p(pp_lat, pp_long)

    vel_x = vel_modulo*np.cos(vel_angulo)
    vel_y =  vel_modulo*np.sin(vel_angulo)

    # calculo el modulo de la velocidad
    modulo_velocidad = np.sqrt(vel_x**2 + vel_y**2) # km por hora
    rotMatrix = np.array([[vel_x/modulo_velocidad, vel_y/modulo_velocidad],
                             [-vel_y/modulo_velocidad,  vel_x/modulo_velocidad]])

    # calculo el alfa (rotacion de la elipse)
    alfa = np.arccos(vel_x/modulo_velocidad) * 180 / np.pi

    # area del fuego deseada
    area_fuego = coef_A*modulo_velocidad + coef_B # 2pi a b

    # excentricidad deseada
    if modulo_velocidad < 5:
        e=0.2
    elif modulo_velocidad < 20:
        e=0.4
    elif modulo_velocidad < 40:
        e=0.6
    elif modulo_velocidad < 80:
        e = 0.8
    else:
        e = 0.9

    # calculamos parametros de la elipse segun el area y la excentricidad.
    a = np.sqrt(np.sqrt(-area_fuego**2 / (4*np.pi**2*(e**2-1))))
    b = area_fuego / (2*np.pi*a)
    c = np.sqrt(a**2 - b**2)

    # centro de la elipse sin rotar con origen en el F1.
    ce_x_elip = c
    ce_y_elip = 0

    # ubicacion del foco que no esta en el origen.
    foco_2_x = 2*c
    foco_2_y = 0

    # rotamos el foco segun el viento.
    foco_2_x_rotado = foco_2_x*vel_y/modulo_velocidad - foco_2_y*vel_x/modulo_velocidad
    foco_2_y_rotado = foco_2_x*vel_x/modulo_velocidad - foco_2_y*vel_y/modulo_velocidad

    # rotamos el centro segun el viento.
    ce_x__elip_rotado = ce_x_elip*vel_y/modulo_velocidad - ce_y_elip*vel_x/modulo_velocidad
    ce_y__elip_rotado = ce_x_elip*vel_x/modulo_velocidad - ce_y_elip*vel_y/modulo_velocidad

    ce_x = ce_x__elip_rotado + fi_x
    ce_y = ce_y__elip_rotado + fi_y

    ce_long, ce_lat = p(ce_x, ce_y, inverse=True)

    # trasladamos la ubicacion de la persona en relacion al foco del incendio (origen)
    x_persona_ellip = pp_x - fi_x
    y_persona_ellip = pp_y - fi_y

    dist_persona_al_foco_1 = np.sqrt(x_persona_ellip**2 + y_persona_ellip**2)
    dist_persona_al_foco_2 = np.sqrt( (x_persona_ellip - foco_2_x_rotado)**2 + ( y_persona_ellip -  foco_2_y_rotado)**2)

    # si la persona no esta en riesgo.
    if not (dist_persona_al_foco_1 + dist_persona_al_foco_2) < 2*a:
        print "person is safe"
        return (ce_y, ce_x, None, None, a, b, alfa)

    print "person is not safe"

    # calculo los puntos de la elipse y buscamos el punto mas cercano.
    # ecuacion parametrica
    t = np.linspace(0, 2*np.pi, 100)
    nel = np.size(t)

    foco_incendio = np.array([[fi_x, fi_y]])
    posicion_persona = np.array([[pp_x, pp_y]])

    # genero vector de unos
    ones = np.ones((nel, 1))

    # Elipse desplazada una distancia C a la derecha.
    Z= np.concatenate( (a*np.cos(t)[:,None], b*np.sin(t)[:,None]),axis=1) + np.dot(ones, np.array([[c, 0]]))
    # a la imagen desplazada la roto.
    E = np.dot(Z, rotMatrix) + np.dot(ones, foco_incendio)

    # calcula la distancia con cada punto de la elipse
    ps_x = None
    ps_y = None
    dst = np.inf
    for index,value in enumerate(t):
        dst_temp = np.sqrt( (posicion_persona[0][0] - E[index][0])**2 + (posicion_persona[0][1] - E[index][1])**2)
        if dst_temp < dst:
            dst = dst_temp
            ps_x = E[index][0]
            ps_y = E[index][1]

    ps_long, ps_lat =  p(ps_x, ps_y, inverse=True)

    punto_salida = np.array([[ps_x, ps_y]])

    # grafico para validar los resultados.
    #pyplot.plot(*zip(*E))
    #pyplot.scatter(*zip(*foco_incendio))
    #pyplot.scatter(*zip(*posicion_persona),c='r' )
    #pyplot.scatter(*zip(*punto_salida))


    return (ce_lat, ce_long, ps_lat, ps_long, a, b, alfa)

# function(fi_lat, fi_long,pp_lat, pp_long,vel_lat, vel_long,coef_A=0.5)
if __name__ == '__main__':
    for angle in range(0,360,90):
        for vel_mod in range(1,100,50):
            ellipse(-33.104597,-64.364401,-33.104597,-64.364401, vel_mod, angle)
    #pyplot.grid()
    #pyplot.savefig('myfig.png')
