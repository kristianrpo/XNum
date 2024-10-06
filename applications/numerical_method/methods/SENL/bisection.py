import math
import pandas as pd
"""

El método de bisección es una técnica numérica para encontrar raíces de ecuaciones no lineales en un intervalo [a,b], donde la función f(x) es continua y se cumple que f(a)×f(b)<0, lo que indica la existencia de al menos una raíz. El proceso consiste en calcular el punto medio m=a+b/2​ y evaluar la función en este punto. Si f(m) es cero, m es la raíz. De lo contrario, se elige el subintervalo [a,m] o [m,b] donde la multiplicación de las funciones cambia de signo, y se repite el proceso hasta aproximar la raíz con la precisión deseada.

"""
def bisection(function_input,interval,tolerance,max_iterations,flag_tolerance):
	# Definición de tabla que contiene todo el proceso
	table = {}
	
	# Inicializamos el contador de iteraciones para controlar el número máximo de iteraciones permitidas (Criterio pesimista).
	current_iteration = 1

	# Inicializamos el error actual con infinito para asegurar que el primer cálculo de error sea significativo.
	current_error = math.inf


	# Evaluamos la función en los extremos del intervalo para verificar si alguno de ellos es una raíz exacta.
	x = interval[0]
	fa = eval(function_input)
	x= interval[1]
	fb = eval(function_input)

	# Si el valor en el extremo inferior es cero, ese punto es una raíz.
	if(fa==0):
		return {"message": "{} es raiz de f(x)".format(interval[0]), "table": {}}
	
	# Si el valor en el extremo superior es cero, ese punto es una raíz.
	elif(fb==0):
		return {"message": "{} es raiz de f(x)".format(interval[1]), "table": {}}
	
	# Si el producto de f(a) y f(b) es negativo, se verifica que existe una raíz en el intervalo según el teorema del valor intermedio, y se permite realizar el metodo de bisección para este caso.
	elif(fa*fb<0):
		# Ejecutamos el proceso de bisección mientras no se exceda el número máximo de iteraciones.
		while (current_iteration<=max_iterations):
			# Almacenamos la información de la iteración actual en la tabla.
			table[current_iteration] = {}

			# Calculamos el punto medio del intervalo actual.
			Xm = (interval[0]+interval[1])/2
			
			# Evaluamos la función en el punto medio.
			x = Xm
			f = eval(function_input)

            # Guardamos los datos de la iteración actual en la tabla.
			table[current_iteration]["i"] = current_iteration
			table[current_iteration]["Xm"] = Xm
			table[current_iteration]["F(Xm)"] = f
			
            # Para la primera iteración, el error se mantiene como infinito (no hay valor previo para comparar).
			if current_iteration==1:
				table[current_iteration]["Error"] = current_error

            # Calculamos el error como la diferencia absoluta entre el punto medio actual y el anterior. (Error de dispersión)
			else:
				if(flag_tolerance):
					current_error = abs(table[current_iteration]["Xm"]-table[current_iteration-1]["Xm"])
					table[current_iteration]["Error"] = current_error
				else:
					current_error = abs((table[current_iteration]["Xm"]-table[current_iteration-1]["Xm"])/table[current_iteration]["Xm"])
					table[current_iteration]["Error"] = current_error
			
            # Si la función evaluada en el punto medio es cero, hemos encontrado la raíz exacta.
			if(f==0):
				return {"message": "{} es raiz de f(x)".format(Xm), "table": table}
			
            # Si el error es menor que la tolerancia especificada, aceptamos el punto medio como una aproximación de la raíz.
			elif(current_error<tolerance):
				return {"message": "{} es una aproximación de la raiz de f(x) con un error de {}".format(Xm,current_error), "table": table}
			
            # Si el producto f(a) * f(Xm) es negativo, la raíz está en el subintervalo [a, Xm].
			elif (fa*f<0):
				interval = [interval[0],Xm]

			# Si el producto f(b) * f(Xm) es negativo, la raíz está en el subintervalo [Xm, b].
			elif (fb*f<0):
				interval= [Xm,interval[1]]
			
			# Se evalua la función en el nuevo intervalo
			x = interval[0]
			fa = eval(function_input)
			x= interval[1]
			fb = eval(function_input)

            # Incrementamos el contador de iteraciones.
			current_iteration+=1

        # Si se alcanza el número máximo de iteraciones sin encontrar una raíz, se retorna un mensaje de fallo.
		return  {"message": "Fracasó en {} iteraciones".format(max_iterations), "table": table}
	
    # Si el producto f(a) * f(b) no es negativo, el intervalo proporcionado no es adecuado para la bisección.
	else:
		return {"message": "El intervalo es inadecuado, recuerde que se debe encontrar un raíz para el intervalo dado".format(max_iterations), "table": {}}