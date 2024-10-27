import numpy as np  # Importa la librería NumPy, que proporciona soporte para arrays y funciones matemáticas.
from src.application.numerical_method.interfaces.matrix_method import MatrixMethod  # Importa la clase base MatrixMethod desde su ubicación.

class GaussSeidelService(MatrixMethod):  # Define la clase GaussSeidelService que hereda de MatrixMethod.
    def solve(  # Define el método solve que resolverá el sistema de ecuaciones lineales usando el método de Gauss-Seidel.
        self,
        A: list[list[float]],  # Matriz de coeficientes, representada como una lista de listas de números flotantes.
        b: list[float],        # Vector de términos independientes, representado como una lista de números flotantes.
        x0: list[float],       # Vector inicial de aproximación, representado como una lista de números flotantes.
        tolerance: float,      # Tolerancia para el error en la aproximación.
        max_iterations: int    # Número máximo de iteraciones permitidas para evitar bucles infinitos.
    ) -> dict:  # Indica que el método devolverá un diccionario.

        # Validación de entradas
        if not self._validate_input(A, b, x0):  # Llama al método de validación de entradas. Si falla, retorna un mensaje de error.
            return {
                "message_method": "Error: Las entradas deben ser numéricas y A debe ser cuadrada de hasta 6x6.",  # Mensaje de error para el usuario.
                "table": {},  # Inicializa una tabla vacía para registrar los resultados.
                "is_successful": False,  # Indica que la operación no fue exitosa.
                "have_solution": False,   # Indica que no se encontró una solución.
                "solution": [],           # Lista vacía para la solución.
            }
        
        # Convierte las listas de entrada a arrays de NumPy para facilitar cálculos.
        A = np.array(A)  # Convierte la matriz de coeficientes en un array de NumPy.
        b = np.array(b)  # Convierte el vector de términos independientes en un array de NumPy.
        x0 = np.array(x0)  # Convierte el vector inicial de aproximación en un array de NumPy.
        
        n = len(b)  # Almacena el tamaño del vector b, que debe ser igual al número de filas de A.
        x1 = x0.copy()  # Crea una copia del vector inicial para almacenar los nuevos valores de las soluciones.
        current_error = tolerance + 1  # Inicializa el error actual para asegurar que la primera comparación sea válida.
        current_iteration = 0  # Contador para las iteraciones actuales.
        table = {}  # Inicializa un diccionario para almacenar los resultados de cada iteración.

        # Bucle principal del método de Gauss-Seidel.
        while current_error > tolerance and current_iteration < max_iterations:  # Mientras el error sea mayor que la tolerancia y no se exceda el máximo de iteraciones.
            # Iteración de Gauss-Seidel
            for i in range(n):  # Recorre cada fila de la matriz A.
                # Calcula la suma de los elementos ya calculados de x1
                sum_others = np.dot(A[i, :i], x1[:i]) + np.dot(A[i, i+1:], x1[i+1:])  # Producto punto para sumar las contribuciones de los otros términos.
                x1[i] = (b[i] - sum_others) / A[i, i]  # Calcula el nuevo valor de x1[i] usando la fórmula de Gauss-Seidel.

            current_error = np.linalg.norm(x1 - x0, ord=np.inf)  # Calcula el error actual como la norma infinita de la diferencia entre x1 y x0.
            
            # Guardamos la información de la iteración actual
            table[current_iteration + 1] = {  # Almacena la información de la iteración actual en la tabla.
                "iteration": current_iteration + 1,  # Número de iteración (empezando desde 1).
                "X": x1.tolist(),  # Convierte el array x1 a lista y lo almacena.
                "Error": current_error,  # Almacena el error actual.
            }
            
            # Preparación para la siguiente iteración
            x0 = x1.copy()  # Actualiza x0 con el nuevo valor de x1 para la próxima iteración.
            current_iteration += 1  # Incrementa el contador de iteraciones.
        
        # Verificación de éxito o fallo tras las iteraciones
        if current_error <= tolerance:  # Si el error es menor o igual a la tolerancia deseada, se considera exitoso.
            return {
                "message_method": f"Aproximación de la solución con tolerancia = {tolerance}",  # Mensaje indicando que se encontró una solución.
                "table": table,  # Retorna la tabla de iteraciones.
                "is_successful": True,  # Indica que la operación fue exitosa.
                "have_solution": True,  # Indica que se encontró una solución.
                "solution": x1.tolist(),  # Retorna la solución como lista.
            }
        elif current_iteration >= max_iterations:  # Si se alcanza el máximo de iteraciones, pero aún no se ha llegado a la tolerancia.
            return {
                "message_method": f"El método funcionó correctamente, pero no se encontró una solución en {max_iterations} iteraciones.",  # Mensaje informando que se alcanzó el límite sin solución.
                "table": table,  # Retorna la tabla de iteraciones.
                "is_successful": True,  # Indica que el método se ejecutó sin errores.
                "have_solution": False,  # Indica que no se encontró solución.
                "solution": x1.tolist(),  # Retorna la última aproximación como solución.
            }
        else:  # Caso donde no se ha podido encontrar solución, pero no por límite de iteraciones.
            return {
                "message_method": f"El método falló al intentar aproximar una solución",  # Mensaje de error informando que no se pudo encontrar solución.
                "table": table,  # Retorna la tabla de iteraciones.
                "is_successful": False,  # Indica que la operación no fue exitosa.
                "have_solution": False,  # Indica que no se encontró solución.
                "solution": [],  # Lista vacía para la solución.
            }

    def _validate_input(self, A, b, x0):  # Define un método privado para validar las entradas.
        # Validar que A es cuadrada y de máximo tamaño 6x6
        if len(A) > 6 or any(len(row) != len(A) for row in A):  # Comprueba que A no exceda 6 filas y que todas las filas tengan el mismo número de columnas.
            return False  # Si falla, retorna False.
        # Validar que b y x0 tengan tamaños compatibles con A
        if len(b) != len(A) or len(x0) != len(A):  # Verifica que los tamaños de b y x0 coincidan con el número de filas de A.
            return False  # Si falla, retorna False.
        # Validar que todos los elementos sean numéricos
        try:
            _ = np.array(A, dtype=float)  # Intenta convertir A a un array de NumPy de tipo float.
            _ = np.array(b, dtype=float)  # Intenta convertir b a un array de NumPy de tipo float.
            _ = np.array(x0, dtype=float)  # Intenta convertir x0 a un array de NumPy de tipo float.
        except ValueError:  # Si ocurre un error durante la conversión (elementos no numéricos).
            return False  # Retorna False.
        return True  # Si todas las validaciones son exitosas, retorna True.
