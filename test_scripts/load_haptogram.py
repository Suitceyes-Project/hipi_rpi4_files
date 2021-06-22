#!/usr/bin/env python

import numpy as np
import time
import os
import datetime
import json
import numpy as np


with open('angry.json') as angry_file:
    data = json.load(angry_file)
    
    #timing = data[0]
    #print(type(data["ftime"]))
    #print(timing)
    #arr = np.array(data["ftime"],dtype=float)
    #print(arr[0])
    print(data["frames"][0]["actuators"])
    arr = np.array(data["frames"][0]["actuators"],dtype=float)
    print(arr[0])
    print(type(data["frames"][1]["time"]))
    print(type(data["counts"]))
    print(len(data["frames"]))
