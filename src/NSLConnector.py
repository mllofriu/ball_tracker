#!/usr/bin/env python

'''
Created on May 22, 2013

@author: mllofriu
'''
import roslib; roslib.load_manifest('visionTests')
import rospy

import socket
import robotProtocol_pb2 as rp
from pilot import Pilot

from sitDown import SitDown
from InfoGatherer import InfoGatherer

class NSLConnector(object):
    '''
    classdocs
    '''

    pilot = 0
    
    def __init__(self):
        rospy.init_node('NSLConnector')
        # Open the socket 
        s = socket.socket()         # Create a socket object
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # Send every packet individually
#        host = socket.gethostname() # Get local machine name
#        print host
        port = 12345                # Reserve a port for your service.
        s.bind(("0.0.0.0", port))        # Bind to the por
        rospy.loginfo( "NSLConnector initialized")
        
        s.listen(5)                 # Now wait for client connection.
#        while True:
        self.con, addr = s.accept()     # Establish connection with client.
        self.processConnection()
        
    def processConnection(self):
        cmd = rp.Command()
        text = self.con.recv(4096)
        cmd.ParseFromString(text)
        
        # Flag that determines the validity of information gathered 
        validInformation = False
        markers = None
        afforances = None
        infoGatherer = InfoGatherer();
        while cmd.command != rp.Command.close:
            if cmd.command == rp.Command.doAction or cmd.command == rp.Command.rotate :
                print "Command",cmd.angle
                if cmd.angle == 0:
                    self.pilot.forwardMeters(.4)
                else:
                    self.pilot.rotateRad(cmd.angle*pi/180)
                validInformation = False
                
                # Send Ok msg
                okMsg = rp.Response()
                okMsg.ok = True;
                self.con.sendall(okMsg.SerializeToString())
#                con.flush()
            elif cmd.command == rp.Command.startRobot:
                print "Start Robot"
                self.pilot = Pilot()
                # Send Ok msg
                okMsg = rp.Response()
                okMsg.ok = True;
                serial = okMsg.SerializeToString()
                print "Largo", len(serial)
                print "Msg", serial
                self.con.sendall(serial)
                print "ok sent"
#                con.flush()
            elif cmd.command == rp.Command.getAffordances:
                print "Affordances"
                if not validInformation:
                    affordances, markers = infoGatherer.gather()
                    validInformation = True
                print "Affordances obtained", affordances
                self.sendAffordances(affordances,self.con)
                print "affordances sent"
            elif cmd.command == rp.Command.isFood:
                print "Is there food?"
            elif cmd.command == rp.Command.getMarcas:
                print "GetMarcas"
                if not validInformation:
                    affordances, markers = infoGatherer.gather()
                    validInformation = True
            
            
            
            text = self.con.recv(4096)
            cmd.ParseFromString(text)
        
        SitDown()
        # Send Ok msg
        okMsg = rp.Response()
        okMsg.ok = True;
        self.con.send(okMsg.SerializeToString())
    
    def sendAffordances(self, affordances, con):    
        affMsg = rp.Affordances()
        for af in affordances:
            affMsg.affordance.append(af)
        
        con.sendall(affMsg.SerializeToString())
    
    def __del__(self):
        self.con.close()
        
if __name__ == "__main__":
    NSLConnector()