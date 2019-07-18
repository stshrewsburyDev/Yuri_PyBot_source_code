"""
Debug Logs For Yuri PyBot
Made By Steven Shrewsbury (AKA: stshrewsburyDev)
"""

def DEBUG(log):
    DEBUG_LOG = "[DEBUG] "
    DEBUG_LOG += log + "\n"
    print(DEBUG_LOG)

def LOG(log):
    DEBUG_LOG = "[LOG] "
    DEBUG_LOG += log
    print(DEBUG_LOG)

def INFO(log):
    DEBUG_LOG = "[INFO] "
    DEBUG_LOG += log + "\n"
    print(DEBUG_LOG)

def ERROR(log):
    DEBUG_LOG = "[ERROR] "
    DEBUG_LOG += str(log)
    print(DEBUG_LOG)
