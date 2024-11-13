from abc import ABC, abstractmethod


class MatrixMethod(ABC):
    @abstractmethod
    def solve(
        self,
        A: list[list[float]],
        b: list[float],
        x0: list[float],
        tolerance: float,
        max_iterations: int,
        **kwargs,
    ) -> dict:
        """
        Método principal que realiza los cálculos del método numérico.
        """
        pass

    @abstractmethod
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
        """
        Valida las entradas del método.

        Parámetros:
        - matrix_a_raw: str -> La matriz de coeficientes en formato de texto.
        - vector_b_raw: str -> El vector b en formato de texto.
        - initial_guess_raw: str -> El vector inicial x0 en formato de texto.
        - tolerance: float -> Tolerancia para la convergencia.
        - max_iterations: int -> Número máximo de iteraciones permitidas.
        - precision_type: str -> Tipo de precisión: "decimals" o "significant_figures".
        - precision_value: int -> Valor de precisión según el tipo.

        Retorna:
        - str -> Mensaje de error si alguna validación falla.
        - dict -> Contiene los datos procesados (matriz A, vector b, vector x0) si todo es válido.
        """
        pass
