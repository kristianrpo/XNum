from abc import ABC, abstractmethod


class NumericalMethod(ABC):
    @abstractmethod
    def solve(self, function_input, interval, tolerance, max_iterations, precision):
        pass
