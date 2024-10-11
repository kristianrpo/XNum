from abc import ABC, abstractmethod


class IterativeMethod(ABC):
    @abstractmethod
    def solve(
        self,
        initial_point: float,
        tolerance: float,
        max_iterations: int,
        precision: int,
        function_f: str,
        function_g: str,
    ) -> dict:
        pass
