import os
import matplotlib.pyplot as plt

def plot_generation(generation, individuals):
    x_values = [individuo.x for individuo in individuals]
    y_values = [individuo.fx for individuo in individuals]

    plt.scatter(x_values, y_values)
    plt.title(f'Generation {generation+1}')
    plt.xlabel('X')
    plt.ylabel('Y')
    
    folder_path = 'generation_plots'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    plt.savefig(os.path.join(folder_path, f'generation_{generation}.png'))
    plt.close()