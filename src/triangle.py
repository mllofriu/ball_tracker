'''
Created on Mar 6, 2013

@author: mllofriu
'''
from euclid import Point, Line, Movement
from numpy import dot

class Triangle(object):
    '''
    Implements a triangle in a planar geometry and a method to decide if a semgents intersects or is contained
    in the triangle of if intersects one of its sides
    '''
    # small meassure
    eps = 1e-10
    
    def __init__(self,vertices):
        self.segments = []
        for i in range(len(vertices)):
            s = Line([vertices[i],vertices[(i+1) % len(vertices)]])
            self.segments.append(s)
        
        self.vertices = vertices
    
    def containedOrIntersect(self, p1, p2):
        return self.inside(p1) or self.inside(p2) or self.traverses(p1,p2)
    
    def traverses(self,p1,p2):
        def belongs(p, s):
            [s1,s2] = s.points()
            return s1.distance_to(p) < s1.distance_to(s2) and s2.distance_to(p) < s2.distance_to(s1)
        
        # If not same side of some of the lines with origin, meassure distance
        floorS = Line(p1,p2)
        for s in self.segments:
#            print s.distance_to(floorS)
            midPoint = floorS.midpoint_to(s)
            if s.distance_to(midPoint) < self.eps:
                intersection = midPoint
#                print s, floorS, intersection, intersection.distance_to(s),intersection.distance_to(floorS)
                # if the intersection belongs to the segment
                if belongs(intersection, s) and belongs(intersection, floorS):
                    return True
        
        return False
    
           
    
    
    def moved(self, m):
        return Triangle([p.moved(m) for p in self.vertices])
    
    def sameSide(self, line, p1,p2):
            m1 = Movement(p1,line).dr
            m2 = Movement(p2,line).dr
#            print dot(m1, m2)
            # Same side if they are same sign
            return dot(m1,m2) >= 0
            
    def inside(self, p):      
          
        res = True 
        for i in range(len(self.vertices)):
#            print self.segments[(i+1)%len(self.segments)], self.vertices[i], p
            res = res and self.sameSide(self.segments[(i+1)%len(self.segments)], self.vertices[i], p)
        
        return res
     
if __name__ == "__main__":
    t = Triangle([Point([0,0,0]),Point([1,1,0]),Point([0,1,0])])
#    print t.inside(Point([0,0,0]))
    print t.containedOrIntersect(Point([1,0,0]), Point([2,0,0]))
    print t.containedOrIntersect(Point([0,0,0]), Point([2,0,0]))
    print t.containedOrIntersect(Point([.3,.5,0]), Point([2,0,0]))
    print t.containedOrIntersect(Point([.3,.5,0]), Point([.4,.6,0]))
    print t.containedOrIntersect(Point([.5,0,0]), Point([.5,20,0]))
    print t.containedOrIntersect(Point([.5,4,0]), Point([.5,20,0]))
    print t.containedOrIntersect(Point([-.5,.5,0]), Point([10,.5,0]))
    print t.containedOrIntersect(Point([-8,.5,0]), Point([-4,.5,0]))
#    t = Triangle([Point([-1,.5,0]),Point([-1,-.5,0]),Point([0,0,0])])
#    print t.containedOrIntersect(Point([1,-.5,0]), Point([1.1,.5,0]))

    t = Triangle([Point([0,0,0]),Point([0.114805, -0.277164, 0]),Point([-0.114805, -0.277164, 0])])
    print t.containedOrIntersect(Point([0.321333676388,0.211012252727,0]), Point([0.29386833911,-0.0239091576102,0]))
    
    