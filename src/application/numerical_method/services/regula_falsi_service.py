import math
from src.application.numerical_method.interfaces.numerical_method import (
    NumericalMethod,
)

"""

El método de regla falsa es una técnica numérica para encontrar raíces de ecuaciones no lineales en un intervalo [a,b], donde la función f(x) es continua y se cumple que f(a)×f(b)<0, lo que indica la existencia de al menos una raíz. El proceso consiste en calcular el punto de intersección de la linea secante entre (a,f(a)) y (b,f(b)) con el eje x (c=(a*f(b)-b*f(a))/(f(b)-f(a))) y evaluar la función en este punto. Si f(c) es cero, c es la raíz. De lo contrario, se elige el subintervalo [a,c] o [c,b] donde la multiplicación de las funciones cambia de signo, y se repite el proceso hasta aproximar la raíz con la precisión deseada.

"""


class RegulaFalsiService(NumericalMethod):
    def solve(
        self,
        function_input: str,
        interval: list[float],
        tolerance: float,
        max_iterations: int,
        precision: int,
    ) -> dict:
        # Definición de tabla que contiene todo el proceso
        table = {}

        # Inicializamos el contador de iteraciones para controlar el número máximo de iteraciones permitidas (Criterio pesimista).
        current_iteration = 1

        # Inicializamos el error actual con infinito para asegurar que el primer cálculo de error sea significativo.
        current_error = math.inf

        # Evaluamos la función en los extremos del intervalo para verificar si alguno de ellos es una raíz exacta.
        try:
            x = interval[0]
            fa = eval(function_input)
            x = interval[1]
            fb = eval(function_input)
        except Exception as e:
            return {
                "message_method": f"Error en la función ingresada, la descripción de este error fué: {str(e)}. Por favor, verifique que la función sea correcta (que use correctamente las funciones de Python, operadores, funciones math, etc., y se utilice la variable x para la misma)",
                "table": {},
                "is_successful": False,
                "have_solution": False,
                "root": 0.0,
            }

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

        # Si el producto de f(a) y f(b) es negativo, se verifica que existe una raíz en el intervalo según el teorema del valor intermedio, y se permite realizar el metodo de regla falsa para este caso.
        elif fa * fb < 0:
            # Ejecutamos el proceso de regla falsa mientras no se exceda el número máximo de iteraciones.
            while current_iteration <= max_iterations:
                # Almacenamos la información de la iteración actual en la tabla.
                table[current_iteration] = {}

                # Calculamos el valor aproximado que se obtiene a partir de la intersección de y=0 y la recta secante utilizando el intervalo actual del intervalo actual.
                Xn = (interval[0] * fb - interval[1] * fa) / (fb - fa)

                # Evaluamos la función en el punto medio.
                x = Xn
                f = eval(function_input)

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

                # Si la función evaluada en el valor aproximado es cero, hemos encontrado la raíz exacta.
                if f == 0:
                    return {
                        "message_method": "{} es raiz de f(x)".format(Xn),
                        "table": table,
                        "is_successful": True,
                        "have_solution": True,
                        "root": Xn,
                    }

                # Si el error es menor que la tolerancia especificada, aceptamos el valor aproximado como una aproximación de la raíz.
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
                fa = eval(function_input)
                x = interval[1]
                fb = eval(function_input)

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

        # Si el producto f(a) * f(b) no es negativo, el intervalo proporcionado no es adecuado para la bisección.
        else:
            return {
                "message_method": "El intervalo es inadecuado, recuerde que se debe encontrar un raíz para el intervalo dado".format(
                    max_iterations
                ),
                "table": {},
                "is_successful": False,
                "have_solution": False,
                "root": 0.0,
            }
