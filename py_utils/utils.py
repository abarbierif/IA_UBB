#libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import cv2

#
def howis(X):
  print("size =",X.shape)
  print("max =",np.max(X))
  print("min =",np.min(X))

#
def pixels_intensities(X, ax, thresh=100, cmap='gray', fontsize=6):
    ax.imshow(X, cmap=cmap)
    N, M = X.shape
    for i in range(N):
        for j in range(M):
            ax.annotate(text=str(round(X[i,j])),
                        fontsize=fontsize, xy=(j,i),
                        horizontalalignment='center',
                        verticalalignment='center',
                        color='white' if X[i,j]<thresh else 'black')
                        
#
def classes_distribution(y, figsize=(5,5), ylim=None, xlim=None, color='#1f77b4', width=0.8, edgecolor='k', hatch='//', labelrotation=None, xlabel='Classes', ylabel='Frequency', title='Classes distribution', facecolor='lightgrey', cmap=None, save_path=None):
    
    if cmap is not None:
        cmap = plt.get_cmap(cmap)
        colors = cmap(np.linspace(0, 1, len(np.unique(y))))
    else:
        colors = [color] * len(np.unique(y))
  
    fig, ax = plt.subplots(1, 1, layout='constrained', figsize=figsize)
    bars = ax.bar(np.unique(y), np.unique(y, return_counts=True)[1], width=width, color=colors, edgecolor=edgecolor, hatch=hatch)
    
    if ylim:
        ax.set_ylim(ylim)
    if xlim:
        ax.set_xlim(xlim)
        
    ax.tick_params(axis='x', labelrotation=labelrotation)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_facecolor(facecolor)
    ax.bar_label(bars, padding=3)

    if save_path:
        fig.savefig(save_path, format='pdf')
    else:
        plt.show()
                        
if __name__ == '__main__':
    print('executed successfully!')