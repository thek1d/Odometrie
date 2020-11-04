'''
Created on Oct 31, 2020

@author: thek1d
'''

import json, math
from Ellipsoid.ellipsoid_calculator import Plotter, Ellipse_Calulator

''' global data strucutre for endresults '''
data = {'mean_values'         : list(tuple()),
        'covariance_matrixes' : [[],[],[],[],[],[],[],[],[],[],[]],
        'eigenvalues'         : list(tuple()),
        'main_axis_sections'  : list(tuple())
        }

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
    pt = Plotter()
    pt.plotMeanPoints(dataset, data)
    
    deltaRoute = ec.calcRouteDifference(delta_sr=dataset['step_size'], delta_sl=dataset['step_size'])
    deltaAngle = ec.calcAngleDifference(delta_sr=dataset['step_size'], delta_sl=dataset['step_size'], 
                                        wheel_distance=dataset['wheel_distance'])
    
    initialCovarianceMatrix      = [[0,0,0],
                                    [0,0,0],
                                    [0,0,0]]
        
    covarianceMatrixPreviousStep = initialCovarianceMatrix
    
    delta_theta = 0
    
    for step in range(dataset['total_steps']+1):
        if step <= dataset['movement_size_1']:
            covarianceMatrixPreviousStep = ec.get_CovarianceMatrix(covarianceMatrixPreviousStep, dataset, deltaRoute, deltaAngle, delta_theta=delta_theta,
                                                                   delta_sr=dataset['step_size'], delta_sl=dataset['step_size'])
        else:
            delta_theta = dataset['rotation']
            covarianceMatrixPreviousStep = ec.get_CovarianceMatrix(covarianceMatrixPreviousStep, dataset, deltaRoute, deltaAngle ,delta_theta=delta_theta,
                                                                   delta_sr=dataset['step_size'], delta_sl=dataset['step_size'])
        
        data['covariance_matrixes'][step].append(covarianceMatrixPreviousStep)
        ellipse = ec.calcSigmaEllipsoids(data, step)
        pt.plotEllipsoid(ellipse)
        
    pt.showPlot()
                   
        
    
    
    
    
    
    
    