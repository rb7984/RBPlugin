import os

__commandname__ = "RBInfo"

def Do():
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, 'html/info.html')
    open(path, 'r')

    return 0

def RunCommand( is_interactive ):
    Do()

    return 0