from pathlib import Path
from datetime import datetime, timedelta
import os

def set_default_path(name = 'stock_futures'):

    path = os.getcwd().split(name)
    path = path[0] + name
    os.chdir(path)

    return  