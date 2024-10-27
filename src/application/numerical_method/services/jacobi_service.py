import numpy as np
from src.application.numerical_method.interfaces.matrix_method import MatrixMethod

class JacobiService(MatrixMethod):
    def solve(
        self,
        A: list[list[float]],       # Matriz de coeficientes
        b: list[float],             # Vector de términos independientes
        x0: list[float],            # Vector inicial de aproximación
        tolerance: float,           # Tolerancia para el error
        max_iterations: int         # Número máximo de iteraciones
    ) -> dict:
        
        # Validación de entradas
        if not self._validate_input(A, b, x0):
            return {
                "message_method": "Error: Las entradas deben ser numéricas y A debe ser cuadrada de hasta 6x6.",
                "table": {},
                "is_successful": False,
                "have_solution": False,
                "solution": [],
            }
        
        A = np.array(A)
        b = np.array(b)
        x0 = np.array(x0)
        
        n = len(b)
        x1 = np.zeros_like(x0)
        current_error = tolerance + 1
        current_iteration = 0
        table = {}

        while current_error > tolerance and current_iteration < max_iterations:
            # Iteración de Jacobi
            for i in range(n):
                sum_others = np.dot(A[i, :i], x0[:i]) + np.dot(A[i, i+1:], x0[i+1:])
                x1[i] = (b[i] - sum_others) / A[i, i]

            current_error = np.linalg.norm(x1 - x0, ord=np.inf)
            
            # Guardamos la información de la iteración actual
            table[current_iteration + 1] = {
                "iteration": current_iteration + 1,
                "X": x1.tolist(),
                "Error": current_error,
            }
            
            # Preparación para la siguiente iteración
            x0 = x1.copy()
            current_iteration += 1
        
        # Verificación de éxito o fallo tras las iteraciones
        if current_error <= tolerance:
            return {
                "message_method": f"Aproximación de la solución con tolerancia = {tolerance}",
                "table": table,
                "is_successful": True,
                "have_solution": True,
                "solution": x1.tolist(),
            }
        elif current_iteration >= max_iterations:
            return {
                "message_method": f"El método funcionó correctamente, pero no se encontró una solución en {max_iterations} iteraciones.",
                "table": table,
                "is_successful": True,
                "have_solution": False,
                "solution": x1.tolist(),
            }
        else:
            return {
                "message_method": f"El método falló al intentar aproximar una solución",
                "table": table,
                "is_successful": False,
                "have_solution": False,
                "solution": [],
            }

    def _validate_input(self, A, b, x0):
        # Validar que A es cuadrada y de máximo tamaño 6x6
        if len(A) > 6 or any(len(row) != len(A) for row in A):
            return False
        # Validar que b y x0 tengan tamaños compatibles con A
        if len(b) != len(A) or len(x0) != len(A):
            return False
        # Validar que todos los elementos sean numéricos
        try:
            _ = np.array(A, dtype=float)
            _ = np.array(b, dtype=float)
            _ = np.array(x0, dtype=float)
        except ValueError:
            return False
        return True
