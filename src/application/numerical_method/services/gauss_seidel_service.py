import numpy as np
import os
from datetime import datetime
from src.application.numerical_method.interfaces.matrix_method import MatrixMethod
import matplotlib.pyplot as plt


class GaussSeidelService(MatrixMethod):
    def solve(
        self,
        A: list[list[float]],
        b: list[float],
        x0: list[float],
        tolerance: float,
        max_iterations: int,
        precision_type: str = "decimals",
        precision_value: int = 2,
    ) -> dict:

        A = np.array(A)
        b = np.array(b)
        x0 = np.array(x0)

        n = len(b)
        x1 = x0.copy()
        current_error = tolerance + 1
        current_iteration = 0
        table = {}

        # Calcular el radio espectral y verificar convergencia
        spectral_radius, converges = self._calculate_spectral_radius(A)
        convergence_message = (
            "El método converge." if converges else "El método no converge."
        )

        # Bucle principal
        while current_error > tolerance and current_iteration < max_iterations:
            for i in range(n):
                sum_others = np.dot(A[i, :i], x1[:i]) + np.dot(A[i, i + 1:], x1[i + 1:])
                x1[i] = (b[i] - sum_others) / A[i, i]

            current_error = np.linalg.norm(x1 - x0, ord=np.inf)

            # Aplicar precisión al guardar en la tabla
            if precision_type == "decimals":
                x1_rounded = [round(val, precision_value) for val in x1]
                current_error_rounded = round(current_error, precision_value)
            elif precision_type == "significant_figures":
                x1_rounded = [float(f"{val:.{precision_value}g}") for val in x1]
                current_error_rounded = float(f"{current_error:.{precision_value}g}")

            table[current_iteration + 1] = {
                "iteration": current_iteration + 1,
                "X": x1_rounded,
                "Error": current_error_rounded,
            }

            x0 = x1.copy()
            current_iteration += 1

        # Resultado final
        result = {
            "message_method": f"Aproximación de la solución con tolerancia = {tolerance}. {convergence_message}",
            "table": table,
            "is_successful": current_error <= tolerance,
            "have_solution": current_error <= tolerance,
            "solution": x1_rounded if current_error <= tolerance else [],
            "spectral_radius": spectral_radius,
        }

        # Graficar si es 2x2
        if n == 2:
            try:
                graph_path = self._plot_2x2(A, b, x1_rounded)
                result["graph_path"] = graph_path
            except Exception as e:
                result["message_method"] += f" (Error al graficar: {e})"

        return result

    def validate_input(
        self,
        matrix_a_raw: str,
        vector_b_raw: str,
        initial_guess_raw: str,
        tolerance: float,
        max_iterations: int,
        precision_type: str = "decimals",
        precision_value: int = 2,
        **kwargs,
    ) -> str | dict:
        try:
            # Validar tolerancia y número máximo de iteraciones
            if tolerance <= 0:
                return "La tolerancia debe ser un número positivo."
            if max_iterations <= 0:
                return "El número máximo de iteraciones debe ser un entero positivo."

            # Validar precisión
            if precision_type not in ["decimals", "significant_figures"]:
                return "El tipo de precisión debe ser 'decimals' o 'significant_figures'."
            if precision_value <= 0:
                return "El valor de precisión debe ser mayor que 0."

            # Procesar matriz A
            A = [
                [float(num) for num in row.strip().split()]
                for row in matrix_a_raw.split(";") if row.strip()
            ]
            if len(A) > 6 or any(len(row) != len(A) for row in A):
                return "La matriz A debe ser cuadrada y de máximo tamaño 6x6."

            # Procesar vector b
            b = [float(num) for num in vector_b_raw.strip().split()]
            if len(b) != len(A):
                return "El vector b debe tener el mismo tamaño que la matriz A."

            # Procesar vector inicial x0
            x0 = [float(num) for num in initial_guess_raw.strip().split()]
            if len(x0) != len(A):
                return "El vector inicial x0 debe tener el mismo tamaño que la matriz A."

            # Retornar datos procesados si todo es válido
            return {"A": A, "b": b, "x0": x0}

        except ValueError:
            return "Error: Todas las entradas deben ser numéricas."

    def _calculate_spectral_radius(self, A: np.ndarray) -> tuple[float, bool]:
        """
        Calcula el radio espectral y determina si el método converge.
        """
        D = np.diag(np.diag(A))
        L = np.tril(A, -1)
        U = np.triu(A, 1)
        T = np.linalg.inv(D - L) @ U
        eigenvalues = np.linalg.eigvals(T)
        spectral_radius = max(abs(eigenvalues))
        return spectral_radius, spectral_radius < 1

    def _plot_2x2(self, A: np.ndarray, b: np.ndarray, solution: list[float]) -> str:
        """
        Genera una gráfica de las líneas del sistema y su intersección.
        Guarda la gráfica en la carpeta static/plots y retorna la ruta relativa.
        """
        x = np.linspace(-10, 10, 400)
        y1 = (b[0] - A[0, 0] * x) / A[0, 1]
        y2 = (b[1] - A[1, 0] * x) / A[1, 1]

        plt.figure(figsize=(8, 6))
        plt.plot(x, y1, label="Ecuación 1", linestyle="--", color="blue")
        plt.plot(x, y2, label="Ecuación 2", linestyle="-.", color="green")
        plt.scatter(solution[0], solution[1], color="red", label="Solución", zorder=5)
        plt.axhline(0, color="black", linewidth=0.5, linestyle="--")
        plt.axvline(0, color="black", linewidth=0.5, linestyle="--")
        plt.legend()
        plt.title("Sistema de ecuaciones 2x2")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid()

        # Generar el nombre del archivo
        filename = f"plot_{np.random.randint(1e6)}.png"
        filepath = f"static/plots/{filename}"
        plt.savefig(filepath)
        plt.close()  # Cerrar la gráfica para liberar memoria
        return f"plots/{filename}"
