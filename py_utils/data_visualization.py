import numpy as np
import matplotlib.pyplot as plt
import os

def display_data(source, rows, cols, path=None, x=None, y=None, display_mode='classes', num_images=None, figsize=(10,10), cmap=None, save_path=None, layout='constrained'):
    match source:
        case 'dir':
            return display_from_dir(path, rows, cols, display_mode, num_images, figsize, cmap, save_path, layout)
        case 'ndarray':
            return display_from_ndarray(x, y, rows, cols, display_mode, num_images, figsize, cmap, save_path, layout)

def display_from_dir(path, rows, cols, display_mode='classes', num_images=None, figsize=(10,10), cmap=None, save_path=None, layout='constrained'):
    '''Function to visualize images from a directory'''
    
    fig, axs = plt.subplots(rows, cols, layout=layout, figsize=figsize)

    match display_mode:
        case 'classes':
            for _, subdirectory in enumerate(os.listdir(path)):
                class_path = os.path.join(path, subdirectory)
                image_path = os.path.join(class_path, np.random.choice(os.listdir(class_path)))
                image = plt.imread(image_path)
                axs.flat[_].imshow(image, cmap=cmap)
                axs.flat[_].set_title(subdirectory)

            for ax in axs.flat:
                ax.set_axis_off()
        
        case 'random':
            for _ in range(num_images):
                subdirectory = np.random.choice(os.listdir(path))
                class_path = os.path.join(path, subdirectory)
                image_path = os.path.join(class_path, np.random.choice(os.listdir(class_path)))
                image = plt.imread(image_path)
                axs.flat[_].imshow(image, cmap=cmap)
                axs.flat[_].set_title(subdirectory)

            for ax in axs.flat:
                ax.set_axis_off()

    if save_path:
        fig.savefig(save_path, format='pdf')
    else:
        plt.show()

def display_from_ndarray(x, y, rows, cols, display_mode='classes', num_images=None, figsize=(10,10), cmap=None, save_path=None, layout='constrained'):
    '''Function to visualize images from a NumPy array'''

    fig, axs = plt.subplots(rows, cols, layout=layout, figsize=figsize)

    match display_mode:
        case 'classes':
            labels = np.unique(y)
            for _, label in enumerate(labels):
                idx = np.random.choice(np.where(y == label)[0])
                axs.flat[_].imshow(x[idx], cmap=cmap)
                axs.flat[_].set_title(label)

            for ax in axs.flat:
                ax.axis('off')
        
        case 'random':
            for _ in range(num_images):
                label = np.random.choice(np.unique(y))
                idx = np.random.choice(np.where(y == label)[0])
                axs.flat[_].imshow(x[idx], cmap=cmap)
                axs.flat[_].set_title(label)

            for ax in axs.flat:
                ax.axis('off')

    if save_path:
        fig.savefig(save_path, format='pdf')
    else:
        plt.show()

if __name__ == '__main__':
    print('Executed successfully!')

    