from abc import ABC, abstractmethod

class MatrixMethod(ABC):
    @abstractmethod
    def solve(
        self,
        A: list[list[float]],    # Matriz de coeficientes
        b: list[float],          # Vector de términos independientes
        x0: list[float],         # Vector inicial de aproximación
        tolerance: float,        # Tolerancia para el error
        max_iterations: int,     # Número máximo de iteraciones
    ) -> dict:
        pass
