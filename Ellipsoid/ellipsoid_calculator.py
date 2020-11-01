'''
Created on Oct 31, 2020

@author: thek1d
'''

import matplotlib.pyplot as plt
import math
import numpy as np

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
            plt.plot(pos_x, pos_y, 'r+')
            
        for row in range(dataset['movement_size_2'] + 1):
            pos_x = pointsMovement2[row][points_coordinates['point_in_x']]
            pos_y = pointsMovement2[row][points_coordinates['point_in_y']]
            plt.plot(pos_x, pos_y, 'b+')
            
        plt.grid(True)
        plt.show()
        

class Ellipse_Calulator():
    
    def __init__(self):
        self._gradientRouteMatrix   = None
        self._gradientPointMatrix   = None
        self._covarianceMatrixDrive = None
    
    def get_CovarianceMatrix(self, covarianceMatrixPreviousStep , dataset, delta_route, delta_angle, delta_sr, delta_sl):
        gradientPointMatrix   = self.__get_gradientPointMatrix(dataset, delta_route, delta_angle)
        gradientRouteMatrix   = self.__get_gradientRouteMatrix(dataset, delta_route, delta_angle)
        covarianceDriveMatrix = self.__get_covarianceDriveMatrix(dataset, delta_sr, delta_sl)
        covarianceMatrix      = self.__calc_covarianceMatrix(gradientPointMatrix, covarianceMatrixPreviousStep, 
                                                             gradientRouteMatrix, covarianceDriveMatrix)
        
        return covarianceMatrix
        
          
    
    def __calc_covarianceMatrix(self, gradientPointMatrix, covarianceMatrixPreviousStep , gradientRouteMatrix, covarianceDriveMatrix):
        covarianceMatrix = np.add((np.matmul(gradientPointMatrix, np.matmul(covarianceMatrixPreviousStep, np.transpose(gradientPointMatrix)))),
                                   np.matmul(gradientRouteMatrix, np.matmul(covarianceDriveMatrix, np.transpose(gradientRouteMatrix))))
        return covarianceMatrix
        

    def __get_gradientPointMatrix(self, dataset, delta_route, delta_angle):
        gradientPointMatrix = [ [1, 0, -delta_route * math.sin(dataset['theta0'] + delta_angle * .5)],
                                [0, 1,  delta_route * math.cos(dataset['theta0'] + delta_angle * .5)],
                                [0, 0,                                                             1]
                              ]
        return gradientPointMatrix
    
    
    def __get_gradientRouteMatrix(self, dataset, delta_route, delta_angle):
        gradientRouteMatrix = [ [.5 * math.cos(dataset['theta0']+ delta_angle * .5)  - delta_route/(2*dataset['wheel_distance']) * math.sin(dataset['theta0'] + delta_angle * .5), 
                                 .5 * math.cos(dataset['theta0']+ delta_angle * .5)  + delta_route/(2*dataset['wheel_distance']) * math.sin(dataset['theta0'] + delta_angle * .5)],
                                [.5 * math.sin(dataset['theta0']+ delta_angle * .5)  + delta_route/(2*dataset['wheel_distance']) * math.cos(dataset['theta0'] + delta_angle * .5),
                                 .5 * math.sin(dataset['theta0']+ delta_angle * .5)  - delta_route/(2*dataset['wheel_distance']) * math.cos(dataset['theta0'] + delta_angle * .5)],
                                [ 1 / dataset['wheel_distance'], -1 / dataset['wheel_distance'] ] 
                              ]
        return gradientRouteMatrix
    
    
    def __get_covarianceDriveMatrix(self, dataset, delta_sr, delta_sl):
        covarianceDriveMatrix = [       [dataset['covariance']['wheel_right'] * math.fabs(delta_sr), 0],
                                        [0, dataset['covariance']['wheel_left'] * math.fabs(delta_sl) ] 
                                ]
        return covarianceDriveMatrix
    
    
    def calcRouteDifference(self, delta_sr, delta_sl):
        return (delta_sr + delta_sl) * 0.5

    def calcAngleDifference(self,delta_sr, delta_sl, wheel_distance):
        return (delta_sr - delta_sl)/wheel_distance      

        
        
             
