def asignar_rango_decada(decade):
    if 1950 <= decade <= 1969:
        return '50s-60s'
    elif 1970 <= decade <= 1989:
        return '70s-80s'
    elif 1990 <= decade <= 2009:
        return '90s-00s'
    else:
        return 'Otros'