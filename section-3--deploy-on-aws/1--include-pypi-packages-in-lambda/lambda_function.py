import json
import os

import numpy as np

def lambda_handler(event: dict, context):
    res = np.array([1, 2, 3, 4, 5]) + np.array([5, 4, 3, 2, 1])
    print(res)
    return event