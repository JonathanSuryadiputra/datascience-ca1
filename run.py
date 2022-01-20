import pandas as pd
import numpy as np
import sys
from Cryptocurrency.api import Api


def __init__(self):
    self.data = None

if __name__ == '__main__':
    getApi = Api()
    data = getApi.getData(2015)
    print(data)