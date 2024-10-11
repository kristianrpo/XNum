import math
from src.application.numerical_method.interfaces.iterative_method import (
    IterativeMethod,
)

"""

El método de punto fijo es una técnica para resolver ecuaciones no lineales. Consiste en reformular la ecuación original f(x)=0 en la forma x=g(x), donde g(x) es una función que se elige para que sus iteraciones sucesivas converjan a una raíz de f(x). A partir de un valor inicial, se evalúa iterativamente g(x), y los valores obtenidos tienden a aproximarse cada vez más a la raíz de la ecuación original.

"""


class FixedPointService(IterativeMethod):
    def solve(
        self,
        initial_point: float,
        tolerance: float,
        max_iterations: int,
        precision: int,
        function_f: str,
        function_g: str,
    ) -> dict:
        # Definición de tabla que contiene todo el proceso
        table = {}

        # Inicializamos el contador de iteraciones para controlar el número máximo de iteraciones permitidas (Criterio pesimista).
        current_iteration = 1

        # Inicializamos el error actual con infinito para asegurar que el primer cálculo de error sea significativo.
        current_error = math.inf

        # Ejecutamos el proceso de punto fijo mientras no se exceda el número máximo de iteraciones.
        while current_iteration <= max_iterations:
            # Almacenamos la información de la iteración actual en la tabla.
            table[current_iteration] = {}

            try:
                # Evaluamos el punto inicial en la función g(x) que es equivalente a f(x)
                x = initial_point
                g = eval(function_g)

                # El resultado de la función g evaluada en el x0 lo evaluamos en f(x)
                x = g
                f = eval(function_f)
            except Exception as e:
                return {
                    "message_method": f"Error en la función ingresada, la descripción de este error fué: {str(e)}. Por favor, verifique que las funciónes sean correctas (que use correctamente las funciones de Python, operadores, funciones math, etc., y se utilice la variable x para las mismas). Adicionalmente verifique su g(x)",
                    "table": {},
                    "is_successful": False,
                    "have_solution": False,
                    "root": 0.0,
                }

            # Guardamos los datos de la iteración actual en la tabla.
            table[current_iteration]["iteration"] = current_iteration
            table[current_iteration]["approximate_value"] = g
            table[current_iteration]["f_evaluated"] = f

            # Para la primera iteración, el error se mantiene como infinito (no hay valor previo para comparar).
            if current_iteration == 1:
                table[current_iteration]["error"] = current_error

            # Calculamos el error como la diferencia absoluta entre el valor aproximado actual y el anterior. (Error de dispersión)
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
                    "message_method": "{} es raiz de f(x)".format(g),
                    "table": table,
                    "is_successful": True,
                    "have_solution": True,
                    "root": g,
                }

            # Si el error es menor que la tolerancia especificada, aceptamos el valor aproximado como una aproximación de la raíz.
            elif current_error < tolerance:
                return {
                    "message_method": "{} es una aproximación de la raiz de f(x) con un error de {}".format(
                        g, current_error
                    ),
                    "table": table,
                    "is_successful": True,
                    "have_solution": True,
                    "root": g,
                }
            else:
                # Se define que el g será para la siguiente iteración el valor para el cual ingresar en g(x)
                initial_point = g

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
