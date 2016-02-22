from django.shortcuts import render

import socket
import json

# Create your views here.
def ovs_echo(HOST, PORT):
    
    #Create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    #Establish TCP session via IP address and port specified
    s.connect((HOST, PORT))
 
    #Send JSON to socket
    print "Sending echo request =====>"
    s.send(json.dumps({'method':'echo','id':'echo','params':[]}))
 
    #Wait for response and print to console
    result = json.loads(s.recv(1024))
    print "<========" + str(result)
    

