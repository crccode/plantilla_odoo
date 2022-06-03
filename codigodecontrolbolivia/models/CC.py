#CC

import sys
from odoo import models, fields, api

import math
import re


def verhoeff(num, times):
	d = [
		[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
		[1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
		[2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
		[3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
		[4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
		[5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
		[6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
		[7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
		[8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
		[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
	]
	p = [
		[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
		[1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
		[5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
		[8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
		[9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
		[4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
		[2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
		[7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
	]
	inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]
	for i in range(times, 0, -1):
		c = 0
		for i in range(len(num)-1, -1, -1):
			c = d[c][p[((len(num) - i) % 8)][int(num[i])]]
		num += str(inv[c])
	return num


def arc4(msg, key):
	state = [i for i in range(256)]
	j = 0
	for i in range(256):
		j = (j + state[i] + ord(key[i % len(key)])) % 256
		temp = state[i]
		state[i] = state[j]
		state[j] = temp
	x = y = 0
	output = ''
	for i in range(len(msg)):
		x = (x + 1) % 256
		y = (state[x] + y) % 256
		temp = state[x]
		state[x] = state[y]
		state[y] = temp
		output += format(ord(msg[i]) ^ state[(state[x] + state[y]) % 256], '02x')
	return output.upper()


def base64(number):
	result = ''
	dic = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/'
	while number > 0:
		result = dic[int(number % 64)] + result
		number = math.floor(number // 64)
	return result


def GenerateControlCode(auth, number, nit, date, monto, key):
	code = ''
	total = str(round(monto+0.001))
	number = verhoeff(number, 2)
	nit = verhoeff(nit, 2)
	date = verhoeff(date, 2)
	total = verhoeff(total, 2)
	vf = verhoeff(str(
		int(number) +
		int(nit) +
		int(date) +
		int(total)
	), 5)[-5:]

	input = [auth, number, nit, date, total]
	idx = 0
	for i in range(5):
		code += input[i] + key[idx:idx+1+int(vf[i])]
		idx += 1+int(vf[i])
	code = arc4(code, key + vf)
	
	final_sum = 0
	total_sum = 0
	partial_sum = [0, 0, 0, 0, 0]
	for i in range(len(code)):
		partial_sum[i % 5] += ord(code[i])
		total_sum += ord(code[i])
	for i in range(5):
		final_sum += math.floor((total_sum * partial_sum[i]) / (1 + int(vf[i])))

	matched = []
	for regexp in re.findall('.{2}', arc4(base64(final_sum), key + vf)):
		matched.append(regexp)
	code = '-'.join(matched)

	return code

def codcontr(Autorizacion, numfacturacc, Nit, Fecha, Monto, Llave):
	codcontrol = {}
	fechacc = {}
	fechastr = {}
	#numfacturacc = ''
	aux1 = 0
	aux2 = 0
	aux3 = 0
	#if context is None:
	#	context = {}
	if	(not Llave or not Monto):
		codcontrol = ''
	else:
	
		if	not Fecha:
			codcontrol = ''
		else:
			if numfacturacc == False:
				codcontrol = ''
			else:
				
				#Volcar la fecha a formato AAAAMMDD sin barras /
				fechastr = str(Fecha)
				fechacc = fechastr[0] + fechastr[1] + fechastr[2] + fechastr[3] + fechastr[5] + fechastr[6] + fechastr[8] + fechastr[9]
				
				#Solo numeros en el numero de factura
				#while	( aux1 < len(Factura) ):
				#		if 	(Factura[aux1].isnumeric()) == True: 
				#			numfacturacc = str(numfacturacc) + str(Factura[aux1])				
				#			aux1 = aux1 + 1						
				#		else:
				#			aux1 = aux1 + 1
				
				#el Nit Existe?
				if 	Nit == False:
					codcontrol = GenerateControlCode( Autorizacion, numfacturacc, '0', fechacc, float(Monto), Llave)					
				else:
					#Solo la parte numerica del Nit
					while (aux2 < len(Nit)):	
						if 	(Nit[aux2].isnumeric()) == True: 
							aux2 = aux2 + 1																
						else:
							aux2 = aux2 + 1
							aux3 = aux3 + 1
										
					#si el nit es solo numeros?	
					if  aux3 == 0:
						codcontrol = GenerateControlCode( Autorizacion, numfacturacc, str(Nit), fechacc, float(Monto), Llave)					
					else:
						codcontrol = "Error, corregir el nit"
			
	return codcontrol

class codigoprueba(models.Model):
    _name = 'codigodecontrolbolivia.codigoprueba'
    _description = 'codigo de prueba'
    autorizacion = fields.Char()
    numfactura = fields.Char()
    nit = fields.Char()
    fecha = fields.Date()
    total = fields.Float()
    llave = fields.Char()
    cc = fields.Char()
    ok = fields.Char(string='Ok', store=True, readonly=True, compute='_CC_Son_iguales')
    codigodecontrol = fields.Char(string='Codigo de Control', store=True, readonly=True, compute='_codigo_de_control')
    
    @api.depends('autorizacion', 'numfactura', 'nit', 'fecha', 'total', 'llave','cc')
    def _CC_Son_iguales(self):
        for r in self:			
            if r.codigodecontrol == r.cc :
                r.ok = 'Si'
            else:
                r.ok = 'No'	
    #Crea el codigodecontrol
    
    @api.depends('autorizacion', 'numfactura', 'nit', 'fecha', 'total', 'llave','cc')
    def _codigo_de_control(self):	
        for r in self:
            r.codigodecontrol = codcontr(r.autorizacion, r.numfactura, r.nit, r.fecha, r.total, r.llave)