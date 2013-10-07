'''
Created on May 22, 2013

@author: mllofriu
'''

class MarkerCalc(object):
    '''
    classdocs
    '''


    def __init__(selfparams):
        '''
        Constructor
        '''
        pass
    
    def calcMarkers(self, visMarkers):
        markerSamples = {}
        for vm in visMarkers:
            if not vm.id in markerSamples.keys():
                markerSamples[vm.id] = []
            
            markerSamples[vm.id] += [vm.pose.position]
        
        averagedMarkers = []
        for k in markerSamples.keys():
            x = 0; y = 0; z = 0;
            for ms in markerSamples[k]:
                x += ms.x
                y += ms.y
                z += ms.z
            x /= markerSamples[k].length
            y /= markerSamples[k].length
            z /= markerSamples[k].length
            averagedMarkers += [(k,x,y,z)]
        
        return averagedMarkers