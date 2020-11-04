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
    
    def plotMeanPoints(self, dataset, data):
                
        for step in range(dataset['movement_size_1'] + 1):
            last_x = dataset['x0'] + step * dataset['step_size'] * math.cos(dataset['theta0'])
            last_y = dataset['y0'] + step * dataset['step_size'] * math.sin(dataset['theta0'])
            ''' storing mean values '''
            self.__pointsMovement1.append((last_x, last_y))
            data['mean_values'].append((last_x, last_y))
                                
        offset_x = last_x
        offset_y = last_y                                                                 
        
        for step in range(dataset['movement_size_2']):
            ''' (step+1) damit ich drehung nicht als schritt mitnehme! '''
            last_x = offset_x + (step+1) * dataset['step_size'] * math.cos(dataset['theta0'] + dataset['rotation'])
            last_y = offset_y + (step+1) * dataset['step_size'] * math.sin(dataset['theta0'] + dataset['rotation'])
            ''' storing mean values '''
            self.__pointsMovement2.append((last_x, last_y))
            data['mean_values'].append((last_x, last_y))
            
        self.__plotPoints(pointsMovement1=self.__pointsMovement1, pointsMovement2=self.__pointsMovement2, dataset=dataset)
    
    def plotEllipsoid(self, ellipse):
        for i in range(len(ellipse[0])):
            #plt.plot(ellipse[0][i], ellipse[1][i], 'o', color='b', linewidth=1)
            plt.plot(ellipse[0][i], ellipse[1][i], 'bo')

 
    
    def __plotPoints(self, pointsMovement1, pointsMovement2, dataset):
    
        plt.title('Sigma Ellipsoid Plotter')
        points_coordinates = {'point_in_x' : 0, 'point_in_y' : 1}
        
        for row in range(dataset['movement_size_1'] + 1):
            pos_x = pointsMovement1[row][points_coordinates['point_in_x']]
            pos_y = pointsMovement1[row][points_coordinates['point_in_y']]
            plt.plot(pos_x, pos_y, 'r+')
            #plt.plot(pos_x, pos_y, '-', color='b', linewidth=1)
            
        #for row in range(dataset['movement_size_2'] + 1):
        for row in range(dataset['movement_size_2']):
            pos_x = pointsMovement2[row][points_coordinates['point_in_x']]
            pos_y = pointsMovement2[row][points_coordinates['point_in_y']]
            plt.plot(pos_x, pos_y, 'b+')
            #plt.plot(pos_x, pos_y, '-', color='r', linewidth=1)
            
    def showPlot(self):
        plt.grid(True)
        plt.show()
            
class Ellipse_Calulator():

    def __init__(self):
        self._gradientRouteMatrix   = None
        self._gradientPointMatrix   = None
        self._covarianceMatrixDrive = None
    
    def get_CovarianceMatrix(self, covarianceMatrixPreviousStep , dataset, delta_route, delta_angle, delta_theta, delta_sr, delta_sl):
        gradientPointMatrix   = self.__get_gradientPointMatrix(dataset, delta_route, delta_angle, delta_theta)
        gradientRouteMatrix   = self.__get_gradientRouteMatrix(dataset, delta_route, delta_angle, delta_theta)
        covarianceDriveMatrix = self.__get_covarianceDriveMatrix(dataset, delta_sr, delta_sl)
        covarianceMatrix      = self.__calc_covarianceMatrix(gradientPointMatrix, covarianceMatrixPreviousStep, 
                                                             gradientRouteMatrix, covarianceDriveMatrix)
        return covarianceMatrix
    
    def calcRouteDifference(self, delta_sr, delta_sl):
        return (delta_sr + delta_sl) * 0.5

    def calcAngleDifference(self,delta_sr, delta_sl, wheel_distance):
        return (delta_sr - delta_sl)/wheel_distance      
    
    def calcSigmaEllipsoids(self, data, step):        
        eigenvalues, eigenvectors = np.linalg.eig(np.linalg.inv(data['covariance_matrixes'][step][0][:2, :2]))
        
        t = np.linspace(0, 2 * np.pi, 50)
                
        vectorlengthcoefficent = np.array((1 / np.sqrt(eigenvalues[0]) * np.cos(t), 
                                           1 / np.sqrt(eigenvalues[1]) * np.sin(t)))
                              
        ellipse = np.transpose(np.add(np.transpose
                                     (np.matmul(eigenvectors, vectorlengthcoefficent)),
                                      np.array(data['mean_values'][step])))
            
        return ellipse
    
    def __calc_covarianceMatrix(self, gradientPointMatrix, covarianceMatrixPreviousStep , gradientRouteMatrix, covarianceDriveMatrix):
        covarianceMatrix = np.add((np.matmul(gradientPointMatrix, np.matmul(covarianceMatrixPreviousStep, np.transpose(gradientPointMatrix)))),
                                   np.matmul(gradientRouteMatrix, np.matmul(covarianceDriveMatrix, np.transpose(gradientRouteMatrix))))
        return covarianceMatrix
        

    def __get_gradientPointMatrix(self, dataset, delta_route, delta_angle, delta_theta):
        gradientPointMatrix = [ [1, 0, -delta_route * math.sin(dataset['theta0'] + delta_theta + delta_angle * .5)],
                                [0, 1,  delta_route * math.cos(dataset['theta0'] + delta_theta + delta_angle * .5)],
                                [0, 0,                                                                           1]
                              ]
        return gradientPointMatrix
    
    
    def __get_gradientRouteMatrix(self, dataset, delta_route, delta_angle, delta_theta):
        gradientRouteMatrix = [ [.5 * math.cos(dataset['theta0']+ delta_theta + delta_angle * .5)  - delta_route/(2*dataset['wheel_distance']) * math.sin(dataset['theta0'] + delta_angle * .5), 
                                 .5 * math.cos(dataset['theta0']+ delta_theta + delta_angle * .5)  + delta_route/(2*dataset['wheel_distance']) * math.sin(dataset['theta0'] + delta_angle * .5)],
                                [.5 * math.sin(dataset['theta0']+ delta_theta + delta_angle * .5)  + delta_route/(2*dataset['wheel_distance']) * math.cos(dataset['theta0'] + delta_angle * .5),
                                 .5 * math.sin(dataset['theta0']+ delta_theta + delta_angle * .5)  - delta_route/(2*dataset['wheel_distance']) * math.cos(dataset['theta0'] + delta_angle * .5)],
                                [ 1 / dataset['wheel_distance'], -1 / dataset['wheel_distance'] ] 
                              ]
        return gradientRouteMatrix
    
    
    def __get_covarianceDriveMatrix(self, dataset, delta_sr, delta_sl):
        covarianceDriveMatrix = [       [dataset['covariance']['wheel_right'] * math.fabs(delta_sr), 0],
                                        [0, dataset['covariance']['wheel_left'] * math.fabs(delta_sl) ] 
                                ]
        return covarianceDriveMatrix
    
    
            
        
    