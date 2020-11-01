'''
Created on Oct 31, 2020

@author: thek1d
'''

import json, math
from Ellipsoid.ellipsoid_calculator import Plotter, Ellipse_Calulator

class Config():
            
    @staticmethod
    def initDataStucture():
        return{
                    'x0'                    : 0,
                    'y0'                    : 0,
                    'step_size'             : 0,
                    'movement_size_1'       : 0,
                    'movement_size_2'       : 0,
                    'movement_size_rotation': 0,
                    'total_steps'           : 0,
                    'theta0'                : math.radians(0),
                    'rotation'              : math.radians(0),
                    'covariance'            : 
                    {
                        'wheel_left' : 0,
                        'wheel_right': 0
                    },
                    'wheel_distance' : 0
              }
    
    @staticmethod
    def readJson(path2JsonFile, dataset):
        file = open(path2JsonFile, 'r')
        data = file.read()
        config = json.loads(data)
        
        dataset['x0']                     = config['x0']
        dataset['y0']                     = config['y0']
        dataset['step_size']              = config['step_size']
        dataset['movement_size_1']        = config['movement_size_1']
        dataset['movement_size_2']        = config['movement_size_2']
        dataset['movement_size_rotation'] = config['movement_size_rotation']
        dataset['total_steps']            = dataset['movement_size_1'] + dataset['movement_size_2']
        dataset['theta0']                 = math.radians(config['theta0'])
        dataset['rotation']               = math.radians(config['rotation'])
        dataset['wheel_distance']         = config['wheel_distance']
                
        covariance = config['covariance']
        
        for elem in range(len(covariance)):
            dataset['covariance']['wheel_left']  = covariance[elem].get('wheel_left')
            dataset['covariance']['wheel_right'] = covariance[elem].get('wheel_right')
        
        
if __name__ == '__main__':
    
    dataset = Config.initDataStucture()
    Config.readJson(path2JsonFile="config.json", dataset=dataset)
         
    
    ec = Ellipse_Calulator()
    
    deltaRoute = ec.calcRouteDifference(delta_sr=dataset['step_size'], delta_sl=dataset['step_size'])
    deltaAngle = ec.calcAngleDifference(delta_sr=dataset['step_size'], delta_sl=dataset['step_size'], 
                                        wheel_distance=dataset['wheel_distance'])
    
    gradienPointMatrix = ec.get_gradientPointMatrix(dataset=dataset, 
                                                    delta_route=deltaRoute, delta_angle=deltaAngle)
    
    gradientRouteMatrix = ec.get_gradientRouteMatrix(dataset=dataset, 
                                                     delta_route=deltaRoute, delta_angle=deltaAngle)
    
    covarianceDriveMatrix = ec.get_covarianceDriveMatrix(dataset=dataset, delta_sr=dataset['step_size'], 
                                                         delta_sl=dataset['step_size'])
    
    gradientRouteMatrix = ec.get_gradientRouteMatrix(dataset=dataset, 
                                                     delta_route=deltaRoute, delta_angle=deltaAngle)
    
    covarianceMatrix = ec.calc_covarianceMatrix(gradienPointMatrix, gradientRouteMatrix, gradientRouteMatrix, gradienPointMatrix)
        
    pt = Plotter()
    pt.plotMeanPoints(dataset=dataset)
    
    
    
    
    
    