__description__ = \
"""
This is a fake gpio interface so that this software can be run and tested
without actually being on a raspberry pi.
"""
__author__ = "Michael J. Harms"
__date__ = "2016-05-20"

def output(*args,**kwargs):

    pass
    #print("WARNING! Using dummy GPIO interface.")

def input(*args,**kwargs):
    #print("WARNING! Using dummy GPIO interface.")
    return 0

class PWM:

    def __init__(self,*args,**kwargs):
        pass
        #print("WARNING! Using dummy GPIO interface.")

    def start(self,*args,**kwargs):
        pass
        #print("WARNING! Using dummy GPIO interface.")

    def stop(self,*args,**kwargs):
        pass
        #print("WARNING! Using dummy GPIO interface.")

def cleanup(*args,**kwargs):
   
    pass 
    #print("WARNING! Using dummy GPIO interface.")

def setup(*args,**kwargs):
    pass
    #print("WARNING! Using dummy GPIO interface.")

def setmode(*args,**kwargs):
    pass
    #print("WARNING! Using dummy GPIO interface.")

def setwarnings(*args,**kwargs):
    pass
    #print("WARNING! Using dummy GPIO interface.")

IN = 0
OUT = 1
BOARD = 0
