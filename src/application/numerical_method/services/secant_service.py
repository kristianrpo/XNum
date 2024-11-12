import math
from src.application.numerical_method.interfaces.interval_method import (
    IntervalMethod,
)

"""
El método de la secante es una técnica numérica para encontrar raíces de ecuaciones no lineales utilizando dos puntos iniciales interval_a y interval_b. La idea es aproximar la raíz mediante la intersección de la recta secante entre (a, f(a)) y (b, f(b)) con el eje x, y luego usar este nuevo punto como base para iterar el proceso hasta alcanzar una tolerancia deseada.
"""


class SecantService(IntervalMethod):
    def solve(
        self,
        x0: float,
        tolerance: float,
        max_iterations: int,
        precision: int,
        function_f: str,
        **kwargs,
    ) -> dict:

        interval_a = x0
        interval_b = kwargs.get("interval_b")

        # Definición de tabla que contiene todo el proceso
        table = {}
        # Inicializamos el contador de iteraciones para controlar el número máximo de iteraciones permitidas.
        current_iteration = 1
        # Inicializamos el error actual con infinito para asegurar que el primer cálculo de error sea significativo.
        current_error = math.inf
        # Evaluamos la función en los puntos iniciales interval_a y interval_b
        x = interval_a
        f_a = eval(function_f)
        x = interval_b
        f_b = eval(function_f)

        # Bucle del método de la secante
        while current_iteration <= max_iterations:
            # Almacenamos la información de la iteración actual en la tabla.
            table[current_iteration] = {}
            # Comprobamos si se puede continuar con la fórmula de la secante
            if f_b - f_a == 0:
                return {
                    "message_method": "Error: División por cero debido a que f(b) y f(a) son iguales.",
                    "table": table,
                    "is_successful": False,
                    "have_solution": False,
                    "root": 0.0,
                }
            # Calculamos el valor aproximado usando la fórmula de la secante
            Xn = interval_b - (f_b * (interval_b - interval_a) / (f_b - f_a))
            # Evaluamos la función en el nuevo valor aproximado
            try:
                x = Xn
                f = eval(function_f)
            except ValueError as ve:
                return {
                    "message_method": f"Error de dominio matemático al evaluar la función en el punto aproximado: {str(ve)}.",
                    "table": table,
                    "is_successful": False,
                    "have_solution": False,
                    "root": 0.0,
                }
            except Exception as e:
                return {
                    "message_method": f"Error al evaluar la función en el punto aproximado: {str(e)}.",
                    "table": {},
                    "is_successful": False,
                    "have_solution": False,
                    "root": 0.0,
                }
            # Guardamos los datos de la iteración actual en la tabla.
            table[current_iteration]["iteration"] = current_iteration
            table[current_iteration]["a"] = interval_a
            table[current_iteration]["b"] = interval_b
            table[current_iteration]["f(a)"] = f_a
            table[current_iteration]["f(b)"] = f_b
            table[current_iteration]["approximate_value"] = Xn
            table[current_iteration]["f_evaluated"] = f
            # Para la primera iteración, el error se mantiene como infinito (no hay valor previo para comparar).
            if current_iteration == 1:
                table[current_iteration]["error"] = current_error
            # Calculamos el error como la diferencia absoluta entre el valor aproximado actual y el anterior.
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
            # Actualizamos los puntos para la siguiente iteración
            interval_a = interval_b
            interval_b = Xn
            # Re-evaluar las funciones en los nuevos puntos
            try:
                x = interval_a
                f_a = eval(function_f)
                x = interval_b
                f_b = eval(function_f)
            except ValueError as ve:
                return {
                    "message_method": f"Error de dominio matemático durante la evaluación en el nuevo intervalo: {str(ve)}.",
                    "table": table,
                    "is_successful": False,
                    "have_solution": False,
                    "root": 0.0,
                }
            except Exception as e:
                return {
                    "message_method": f"Error durante la evaluación en el nuevo intervalo: {str(e)}.",
                    "table": table,
                    "is_successful": False,
                    "have_solution": False,
                    "root": 0.0,
                }
            # Incrementamos el contador de iteraciones.
            current_iteration += 1
        # Si se alcanzó el número máximo de iteraciones sin encontrar una raíz, se retorna un mensaje de fallo.
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
        x0: float,
        tolerance: float,
        max_iterations: int,
        function_f: str,
        **kwargs,
    ) -> str | bool:
        interval_a = x0
        interval_b = kwargs.get("interval_b")

        # Validación de los parámetros de entrada tolerancia positiva
        if not isinstance(tolerance, (int, float)) or tolerance <= 0:
            return "La tolerancia debe ser un número positivo"

        # Validación de los parámetros de entrada maximo numero de iteraciones positivo
        if not isinstance(max_iterations, int) or max_iterations <= 0:
            return "El máximo número de iteraciones debe ser un entero positivo."

        # Evaluamos la función en los puntos iniciales interval_a y interval_b
        try:
            x = interval_a
            f_a = eval(function_f)
            x = interval_b
            f_b = eval(function_f)
        except ValueError as ve:
            return f"Error de dominio matemático al evaluar la función: {str(ve)}. Asegúrese de que los valores iniciales están en el dominio válido de la función."
        except Exception as e:
            return f"Error en la función ingresada, la descripción de este error fue: {str(e)}. Por favor, verifique que la función sea correcta (que use correctamente las funciones de Python, operadores, funciones math, etc., y se utilice la variable x para la misma)"

        return True
