import numpy as np
from config.settings import BASE_DIR
import matplotlib.pyplot as plt
import math

"""
Función que se encarga de generar un archivo vectorizado de la gráfica de una función matemática.
Un archivo vectorizado es un tipo de archivo gráfico que almacena imágenes usando vectores en lugar de píxeles. Los gráficos vectorizados se definen mediante formas geométricas como líneas, curvas, círculos, y polígonos, descritos matemáticamente a través de fórmulas.
"""


def plot_function(function_input: str, have_solution: bool, root: float) -> None:
    output_file = BASE_DIR / "static/img/numerical_method/function_plot.svg"

    # Se crea una figura de tamaño 6x4 pulgadas, es como el lienzo sobre el cual se pinta el gráfico.
    plt.figure(figsize=(6, 4))

    # Generamos un rango de valores para 'x'. Esto quiero decir que vamos a evaluar la función en un rango de valores de 'x' para poder graficarla.
    # Este rango de valores se permite generar utilizando np.linspace donde permite obtener un array de valores de un intervalo, de manera equiespaciada según la cantidad de valores que se necesiten para ese intervalo.
    if not have_solution:
        x_vals = np.linspace(-100, 100, 1000)
    else:
        x_vals = np.linspace(root - 3, root + 3, 1000)
        # Se grafican los puntos de intersección con y = 0, para las raices que son numeros reales y que se encuentran en el intervalo.
        plt.plot(root, 0, marker="o", color="#f7dc6f")
        plt.text(root, 0, f"({root}, 0)", fontsize=9, verticalalignment="bottom")

    # Evaluamos la función en el rango de valores de 'x' que generamos anteriormentey almacenamos cada resultado en una lista.
    y_vals = [eval(function_input, {"math": math, "x": val}) for val in x_vals]

    # Ajustar los límites de los ejes para el recuadro de la grafica como tal
    plt.xlim(root - 5, root + 5)  # Ajusta el rango horizontal para una vista más amplia
    plt.ylim(-4, 4)  # Ajusta el rango vertical para una vista más centrada

    # Se grafica la función con el conjunto de x's y y's que generamos anteriormente en el rango especificado.
    plt.plot(x_vals, y_vals, color="#a18262")
    # Se establece una linea punteada roja en y=0 para identificar la raíz.
    plt.axhline(y=0, color="red", linestyle="--", linewidth=1)
    # Se establece una etiqueta para identificar eje 'x'.
    plt.xlabel("x")
    # Se establece una etiqueta para identificar eje 'y'.
    plt.ylabel("y")
    # Se establece el titulo de la grafica en la parte superior de la misma.
    plt.title(f"y = {function_input}")
    # Se establece que aparezca una cuadricula en el gráfico donde va la función.
    plt.grid(True)

    # Guardamos la gráfica en un archivo SVG
    plt.savefig(output_file, format="svg")
    plt.close()
