'''
Created on Oct 31, 2020

@author: thek1d
'''

import matplotlib.pyplot as plt
import math

class Plotter():
    
    def __init__(self):
        self.__pointsMovement1 = list(tuple())
        self.__pointsMovement2 = list(tuple())
    
    def plotMeanPoints(self, dataset):
        
        for step in range(dataset['movement_size_1'] + 1):
            last_x = dataset['x0'] + step * dataset['step_size'] * math.cos(dataset['theta0'])
            last_y = dataset['y0'] + step * dataset['step_size'] * math.sin(dataset['theta0'])
            ''' storing mean values '''
            self.__pointsMovement1.append((last_x, last_y))
                                
        offset_x = last_x
        offset_y = last_y                                                                 
        
        for step in range(dataset['movement_size_2'] + 1):
            last_x = offset_x + step * dataset['step_size'] * math.cos(dataset['theta0'] + dataset['rotation'])
            last_y = offset_y + step * dataset['step_size'] * math.sin(dataset['theta0'] + dataset['rotation'])
            ''' storing mean values '''
            self.__pointsMovement2.append((last_x, last_y))
            
        self.__plotPoints(pointsMovement1=self.__pointsMovement1, pointsMovement2=self.__pointsMovement2, dataset=dataset)
    
    
    def __plotPoints(self, pointsMovement1, pointsMovement2, dataset):
    
        points_coordinates = {'point_in_x' : 0, 'point_in_y' : 1}
        
        for row in range(dataset['movement_size_1'] + 1):
            pos_x = pointsMovement1[row][points_coordinates['point_in_x']]
            pos_y = pointsMovement1[row][points_coordinates['point_in_y']]
            plt.plot(pos_x, pos_y, 'rx')
            
        for row in range(dataset['movement_size_2'] + 1):
            pos_x = pointsMovement2[row][points_coordinates['point_in_x']]
            pos_y = pointsMovement2[row][points_coordinates['point_in_y']]
            plt.plot(pos_x, pos_y, 'bx')
            
        plt.grid(True)
        plt.show()
        
        
