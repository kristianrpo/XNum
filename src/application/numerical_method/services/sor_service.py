import numpy as np
from src.application.numerical_method.interfaces.matrix_method import MatrixMethod

class SORService(MatrixMethod):
    def solve(
        self,
        A: list[list[float]],       # Matriz de coeficientes
        b: list[float],             # Vector de términos independientes
        x0: list[float],            # Vector inicial de aproximación
        tolerance: float,           # Tolerancia para el error
        max_iterations: int,        # Número máximo de iteraciones
        w: float                    # Factor de relajación
    ) -> dict:
        
        # Validación de entradas
        if not self.validate_input(A, b, x0):
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
        x = x0.copy()
        table = {}

        # Inicialización de matrices para el cálculo de T y C
        D = np.diag(np.diag(A))
        L = -np.tril(A, -1)
        U = -np.triu(A, 1)
        
        # Cálculo de la matriz de iteración T para el método SOR
        T = np.linalg.inv(D - w * L) @ ((1 - w) * D + w * U)
        spectral_radius = max(abs(np.linalg.eigvals(T)))

        current_error = tolerance + 1
        current_iteration = 0

        # Iteración SOR
        while current_error > tolerance and current_iteration < max_iterations:
            x_new = x.copy()
            for i in range(n):
                sum_others = np.dot(A[i, :i], x_new[:i]) + np.dot(A[i, i+1:], x[i+1:])
                x_new[i] = (1 - w) * x[i] + (w / A[i, i]) * (b[i] - sum_others)

            # Calcular el error como norma infinito de la diferencia
            current_error = np.linalg.norm(x_new - x, ord=np.inf)

            # Guardar información en la tabla para la iteración actual
            table[current_iteration + 1] = {
                "iteration": current_iteration + 1,
                "X": x_new.tolist(),
                "Error": current_error,
            }

            # Preparar para la siguiente iteración
            x = x_new
            current_iteration += 1

        # Verificación de éxito o fallo tras las iteraciones
        if current_error <= tolerance:
            return {
                "message_method": f"Aproximación de la solución con tolerancia = {tolerance} y el radio espectral es de = {spectral_radius}",
                "table": table,
                "is_successful": True,
                "have_solution": True,
                "solution": x.tolist(),
                "spectral_radius": spectral_radius,
            }
        elif current_iteration >= max_iterations:
            return {
                "message_method": f"El método funcionó correctamente, pero no se encontró una solución en {max_iterations} iteraciones.",
                "table": table,
                "is_successful": True,
                "have_solution": False,
                "solution": x.tolist(),
                "spectral_radius": spectral_radius,
            }
        else:
            return {
                "message_method": f"El método falló al intentar aproximar una solución",
                "table": table,
                "is_successful": False,
                "have_solution": False,
                "solution": [],
                "spectral_radius": spectral_radius,
            }

    def validate_input(self, A, b, x0):
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
