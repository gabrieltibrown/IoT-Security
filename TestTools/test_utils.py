from gmud_decode import *

def getEndpoints(f):
    inRules, outRules = fileToRules(f)
    return outRules


