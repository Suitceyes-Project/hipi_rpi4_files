#!/usr/bin/env python

import numpy as np
import time
import os
from adafruit_servokit import ServoKit
pca1 = ServoKit(channels=16, address=0x41)

min_pw = 0
max_pw = 11500

pca1.servo[15].set_pulse_width_range(min_pw, max_pw)

pca1.servo[15].angle = 180

