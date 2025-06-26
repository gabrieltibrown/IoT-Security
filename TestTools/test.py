#test script by Gabriel Brown
#takes url to MUDFile as optional command line arg
#defaults to pretending to be an amazon echo

#---------------------------------------------------------#
#             testing options set here
#---------------------------------------------------------#

#test can send a dhcp packet with option 161 or not, depending on what use case is being tested
has_op_161 = True

#the URL to the MUD file that the test is pretending to be when generating traffic
#the test needs a MUD file regardless of it sending the DHCP with option 161
#this is because the test needs some set of rules on how to generate traffic
#MUD URL can be passed as a command line arg
default_mud_url = 'https://raw.githubusercontent.com/iot-onboarding/mudfiles/master/unsw/amazonEchoMud.json'

mud_filepath = 'AmazonEcho.json'

#test can sleep between sending DHCP discover packet and testing endpoints
#one might do this because the IoT gateway takes a significant amount of time to implement Firewall rules
#this may be acceptable but must be disclosed
sleep_time = 10

#test will stop waiting for a response to packets sent after this number of seconds
timeout = 5

#forbidden endpoints to test
forbidden = [['tcp','80','google.com'],['tcp','80','facebook.com']]

#---------------------------------------------------------#
#                     code begins here
#---------------------------------------------------------#

from scapy.all import *
import time
import sys
from test_utils import *
from test_devices import *

#------------------------------DHCP Begin----------------------------#
if(len(sys.argv)>1):
    if sys.argv[1] in config:
        mud_filepath = "MUDfiles/"+sys.argv[1]
        mud_url = config[sys.argv[1]]
        print(mud_filepath + "    " + mud_url)
    else:
        print("not a recognized device. try one of the following: ")
        for key in config:
            print(key)
        exit()
else:
    mud_url = default_mud_url

if(has_op_161):
    conf.checkIPaddr = False
    fam,hw = get_if_raw_hwaddr(conf.iface)
    #dhcp packet here
    dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=hw)/DHCP(options=[("message-type","discover"), (161,mud_url),"end"])
    srp1(dhcp_discover, timeout = timeout)

time.sleep(sleep_time)

#-----------------------------------allowed endpoint test begin-----------------------#
print("starting allowed endpoint test")
allowed_endpoint_failure = 0
#begin generating traffic
allowed_endPoints = getEndpoints(mud_filepath)
tested_endpoints = 0
allowed_fail = []
allowed_pass = []

for endPoint in allowed_endPoints:
    protocol = endPoint[0]
    dport = int(endPoint[1])
    domain = endPoint[2]

    if(protocol == 'tcp'):
        packet = IP(dst=domain)/TCP(dport=dport) 
        tested_endpoints+=1
    elif(protocol == 'udp'):
        #currently no support for testing udp endpoints
        #packet = IP(dst=domain)/UDP(dport=dport)
        continue
    else:
        #print("unknown protocol: " + protocol)
        #print("please update code")
        continue

    ans = sr1(packet, timeout=timeout)

    if(ans == None):
        allowed_endpoint_failure += 1
        allowed_fail.append(endPoint)
    else:
        allowed_pass.append(endPoint)

#------------------------forbidden endpoint test begin------------------------------#
print("begin forbidden endpoint test")
endPoints = forbidden
forbidden_endpoint_failure = 0
forbidden_fail = []
for endPoint in endPoints:
    protocol = endPoint[0]
    dport = int(endPoint[1])
    domain = endPoint[2]

    if(protocol == 'tcp'):
        packet = IP(dst=domain)/TCP(dport=dport) 
    elif(protocol == 'udp'):
        packet = IP(dst=domain)/UDP(dport=dport)
    else:
        print("unknown protocol: " + protocol)
        print("please update code")
        continue

    ans = sr1(packet, timeout=timeout)

    if(ans != None):
        forbidden_endpoint_failure += 1
        forbidden_fail.append(endPoint)

print("")
print('----------------------------------------------------------------------')
print("TEST RESULTS:")

print("ALLOWED ENDPOINT TEST:")
if(allowed_endpoint_failure == 0):
    print("Allowed Endpoint test passed!")
else:
    print("test failed on "+str(allowed_endpoint_failure)+" of "+str(tested_endpoints)+" endpoints")
    for fail in allowed_fail:
        print(str(fail))
    print("test passed for the following endpoints:")
    for passed in allowed_pass:
        print(str(passed))
print("")
print("FORBIDDEN ENDPOINT TEST:")

if(forbidden_endpoint_failure == 0):
    print("Forbidden Endpoint test passed!")
else:
    print("test failed on "+str(forbidden_endpoint_failure)+" of "+str(len(endPoints))+" endpoints")
    for fail in forbidden_fail:
        print(str(fail))


