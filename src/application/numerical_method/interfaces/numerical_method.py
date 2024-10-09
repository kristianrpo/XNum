from abc import ABC, abstractmethod


class NumericalMethod(ABC):
    @abstractmethod
    def solve(
        self,
        function_input: str,
        interval: list[float],
        tolerance: float,
        max_iterations: int,
        precision: int,
    ) -> dict:
        pass
