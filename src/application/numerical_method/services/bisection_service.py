import math
from src.application.numerical_method.interfaces.interval_method import (
    IntervalMethod,
)

"""

El método de bisección es una técnica numérica para encontrar raíces de ecuaciones no lineales en un intervalo [a,b], donde la función f(x) es continua y se cumple que f(a)×f(b)<0, lo que indica la existencia de al menos una raíz. El proceso consiste en calcular el punto medio m=a+b/2​ y evaluar la función en este punto. Si f(m) es cero, m es la raíz. De lo contrario, se elige el subintervalo [a,m] o [m,b] donde la multiplicación de las funciones cambia de signo, y se repite el proceso hasta aproximar la raíz con la precisión deseada.

"""


class BisectionService(IntervalMethod):
    def solve(
        self,
        interval_a: float,
        interval_b: float,
        tolerance: float,
        max_iterations: int,
        function_f: str,
        precision: int,
    ) -> dict:

        # Definición del intervalo inicial.
        interval = [interval_a, interval_b]

        # Definición de tabla que contiene todo el proceso
        table = {}

        # Inicializamos el contador de iteraciones para controlar el número máximo de iteraciones permitidas (Criterio pesimista).
        current_iteration = 1

        # Inicializamos el error actual con infinito para asegurar que el primer cálculo de error sea significativo.
        current_error = math.inf

        # Evaluamos la función en los extremos del intervalo para verificar si alguno de ellos es una raíz exacta.
        x = interval[0]
        fa = eval(function_f)
        x = interval[1]
        fb = eval(function_f)

        # Si el valor en el extremo inferior es cero, ese punto es una raíz.
        if fa == 0:
            return {
                "message_method": "{} es raiz de f(x) y es el extremo inferior del intervalo".format(
                    interval[0]
                ),
                "table": {},
                "is_successful": True,
                "have_solution": True,
                "root": interval[0],
            }

        # Si el valor en el extremo superior es cero, ese punto es una raíz.
        elif fb == 0:
            return {
                "message_method": "{} es raiz de f(x) y es el extremo superior del intervalo".format(
                    interval[1]
                ),
                "table": {},
                "is_successful": True,
                "have_solution": True,
                "root": interval[1],
            }

        # Ejecutamos el proceso de bisección mientras no se exceda el número máximo de iteraciones.
        while current_iteration <= max_iterations:
            # Almacenamos la información de la iteración actual en la tabla.
            table[current_iteration] = {}

            # Calculamos el punto medio del intervalo actual.
            Xn = (interval[0] + interval[1]) / 2

            # Evaluamos la función en el punto medio.
            x = Xn
            f = eval(function_f)

            # Guardamos los datos de la iteración actual en la tabla.
            table[current_iteration]["iteration"] = current_iteration
            table[current_iteration]["approximate_value"] = Xn
            table[current_iteration]["f_evaluated"] = f

            # Para la primera iteración, el error se mantiene como infinito (no hay valor previo para comparar).
            if current_iteration == 1:
                table[current_iteration]["error"] = current_error

            # Calculamos el error como la diferencia absoluta entre el punto medio actual y el anterior. (Error de dispersión)
            else:
                if precision:
                    current_error = abs(
                        table[current_iteration]["approximate_value"]
                        - table[current_iteration - 1]["approximate_value"]
                    )
                    table[current_iteration]["error"] = current_error
                else:
                    current_error = abs(
                        (
                            table[current_iteration]["approximate_value"]
                            - table[current_iteration - 1]["approximate_value"]
                        )
                        / table[current_iteration]["approximate_value"]
                    )
                    table[current_iteration]["error"] = current_error

            # Si la función evaluada en el punto medio es cero, hemos encontrado la raíz exacta.
            if f == 0:
                return {
                    "message_method": "{} es raiz de f(x)".format(Xn),
                    "table": table,
                    "is_successful": True,
                    "have_solution": True,
                    "root": Xn,
                }

            # Si el error es menor que la tolerancia especificada, aceptamos el punto medio como una aproximación de la raíz.
            elif current_error < tolerance:
                return {
                    "message_method": "{} es una aproximación de la raiz de f(x) con un error de {}".format(
                        Xn, current_error
                    ),
                    "table": table,
                    "is_successful": True,
                    "have_solution": True,
                    "root": Xn,
                }

            # Si el producto f(a) * f(Xn) es negativo, la raíz está en el subintervalo [a, Xn].
            elif fa * f < 0:
                interval = [interval[0], Xn]

            # Si el producto f(b) * f(Xn) es negativo, la raíz está en el subintervalo [Xn, b].
            elif fb * f < 0:
                interval = [Xn, interval[1]]

            # Se evalua la función en el nuevo intervalo
            x = interval[0]
            fa = eval(function_f)
            x = interval[1]
            fb = eval(function_f)

            # Incrementamos el contador de iteraciones.
            current_iteration += 1

        # Si se alcanza el número máximo de iteraciones sin encontrar una raíz, se retorna un mensaje de fallo.
        return {
            "message_method": "El método funcionó correctamente pero no se encontró solución para {} iteraciones".format(
                max_iterations
            ),
            "table": table,
            "is_successful": True,
            "have_solution": False,
            "root": 0.0,
        }            
        
    def validate_input(
        self,
        interval_a: float,
        interval_b: float,
        tolerance: float,
        max_iterations: int,
        function_f: str,
    ) -> str | bool:
        
        # Validación de los parámetros de entrada tolerancia positiva
        if not isinstance(tolerance, (int, float)) or tolerance <= 0:
            return "La tolerancia debe ser un número positivo"
        
        # Validación de los parámetros de entrada maximo numero de iteraciones positivo
        if not isinstance(max_iterations, int) or max_iterations <= 0:
            return "El máximo número de iteraciones debe ser un entero positivo."
        
        # Validación de la función ingresada
        try:
            x = interval_a
            fa = eval(function_f)
            x = interval_b
            fb = eval(function_f) 
        except Exception as e:
            return f"Error en la función ingresada, la descripción de este error fue: {str(e)}. Por favor, verifique que la función sea correcta (que use correctamente las funciones de Python, operadores, funciones math, etc, y se utilice la variable x para la misma)."
                
        
        # Si el producto f(a) * f(b) no es negativo, el intervalo proporcionado no es adecuado para la bisección.
        if fa*fb>0:
            return "El intervalo es inadecuado, recuerde que se debe encontrar un raíz para el intervalo dado".format(max_iterations)
        
        return True
