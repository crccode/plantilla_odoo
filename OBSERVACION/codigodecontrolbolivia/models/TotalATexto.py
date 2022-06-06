
# -------------------------------------------------------------
# Español
# -------------------------------------------------------------

hasta_19 = ( 'CERO',  'UNO',   'DOS',  'TRES', 'CUATRO',   'CINCO',   'SEIS',
          'SIETE', 'OCHO', 'NUEVE', 'DIEZ',   'ONCE', 'DOCE', 'TRECE',
          'CATORCE', 'QUINCE', 'DIECISEIS', 'DIECISIETE', 'DIECIOCHO', 'DIECINUEVE', 'VEINTE', 'VEINTIUN', 'VEINTIDOS', 'VEINTITRES', 'VEINTICUATRO', 'VEINTICINCO', 'VEINTISEIS', 'VEINTISIETE', 'VEINTIOCHO', 'VEINTINUEVE' )

decenas  = ( 'TREINTA', 'CUARENTA', 'CINCUENTA', 'SESENTA', 'SETENTA', 'OCHENTA', 'NOVENTA', 'CIEN')

hasta_19x = ( 'CERO',  'UN',   'DOS',  'TRES', 'CUATRO',   'CINCO',   'SEIS',
          'SIETE', 'OCHO', 'NUEVE', 'DIEZ',   'ONCE', 'DOCE', 'TRECE',
          'CATORCE', 'QUINCE', 'DIECISEIS', 'DIECISIETE', 'DIECIOCHO', 'DIECINUEVE', 'VEINTE', 'VEINTIUN', 'VEINTIDOS', 'VEINTITRES', 'VEINTICUATRO', 'VEINTICINCO', 'VEINTISEIS', 'VEINTISIETE', 'VEINTIOCHO', 'VEINTINUEVE' )

centenas = ( '',   'CIENTO',  'DOSCIENTOS',   'TRESCIENTOS',   'CUATROCIENTOS', 'QUINIENTOS',   'SEISCIENTOS',   'SETECIENTOS',   'OCHOCIENTOS',  'NOVECIENTOS',   'UN MIL')

millares = ( '',
          'MIL',     'MILLONES',         'MIL MILLONES',       'Trillion',       'Quadrillion',
          'Quintillion',  'Sextillion',      'Septillion',    'Octillion',      'Nonillion',
          'Decillion',    'Undecillion',     'Duodecillion',  'Tredecillion',   'Quattuordecillion',
          'Sexdecillion', 'Septendecillion', 'Octodecillion', 'Novemdecillion', 'Vigintillion' )

def _convertir_nn(valor):
    """convert a valorue < 100 to English.
    """
    if valor < 30:
        return hasta_19[valor]
    for (dcap, dvalor) in ((k, 30 + (10 * v)) for (v, k) in enumerate(decenas)):
        if dvalor + 10 > valor:
            if valor % 10:
                return dcap + ' y ' + hasta_19[valor % 10]
            return dcap

def _convertir_nnx(valor):
    """convert a valorue < 100 to English.
    """
    if valor < 30:
        return hasta_19x[valor]
    for (dcap, dvalor) in ((k, 30 + (10 * v)) for (v, k) in enumerate(decenas)):
        if dvalor + 10 > valor:
            if valor % 10:
                return dcap + ' y ' + hasta_19x[valor % 10]
            return dcap


def _convertir_nnn(valor):
    """
        convert a valorue < 1000 to english, special cased because it is the level that kicks 
        off the < 100 special case.  The rest are more general.  This also allows you to
        get strings in the form of 'forty-five hundred' if called directly.
    """
    palabra = ''
    (mod, rem) = (valor % 100, valor // 100)
    if rem > 0:
        palabra = centenas[rem]
        if mod > 0:
            palabra += ' '
    if mod > 0:
        palabra += _convertir_nn(mod)
    return palabra

def _convertir_nnnx(valor):
    """
        convert a valorue < 1000 to english, special cased because it is the level that kicks 
        off the < 100 special case.  The rest are more general.  This also allows you to
        get strings in the form of 'forty-five hundred' if called directly.
    """
    palabra = ''
    (mod, rem) = (valor % 100, valor // 100)
    if rem > 0:
        palabra = centenas[rem]
        if mod > 0:
            palabra += ' '
    if mod > 0:
        palabra += _convertir_nnx(mod)
    return palabra


def entero_a_texto(valor):
    if valor < 101:
        return _convertir_nn(valor)
    if valor < 1001:
         return _convertir_nnn(valor)
    for (didx, dvalor) in ((v - 1, 1000 ** v) for v in range(len(millares))):
        if dvalor > valor:
            mod = 1000 ** didx
            l = valor // mod
            r = valor - (l * mod)
            ret = _convertir_nnnx(l) + ' ' + millares[didx]
            if r > 0:
                ret = ret + ' ' + entero_a_texto(r)
            return ret

def totalliteral(monto, moneda):
    monto = '%.2f' % monto
    list = str(monto).split('.')
    texto_entero = entero_a_texto(int(list[0]))
    centavos = str(list[1])
    
    
    return ' '.join(filter(None, [texto_entero, centavos, '/100', str(moneda).replace('BOB','Bolivianos.')]))
