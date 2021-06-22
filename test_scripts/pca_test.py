from adafruit_servokit import ServoKit
pca = ServoKit(channels=16)

min_pw = 0
max_pw = 11500

pca.servo[0].set_pulse_width_range(min_pw, max_pw)
pca.servo[1].set_pulse_width_range(min_pw, max_pw)
pca.servo[2].set_pulse_width_range(min_pw, max_pw)
pca.servo[3].set_pulse_width_range(min_pw, max_pw)
pca.servo[4].set_pulse_width_range(min_pw, max_pw)
pca.servo[5].set_pulse_width_range(min_pw, max_pw)
pca.servo[6].set_pulse_width_range(min_pw, max_pw)
pca.servo[7].set_pulse_width_range(min_pw, max_pw)
pca.servo[8].set_pulse_width_range(min_pw, max_pw)
pca.servo[9].set_pulse_width_range(min_pw, max_pw)
pca.servo[10].set_pulse_width_range(min_pw, max_pw)
pca.servo[11].set_pulse_width_range(min_pw, max_pw)
pca.servo[12].set_pulse_width_range(min_pw, max_pw)
pca.servo[13].set_pulse_width_range(min_pw, max_pw)
pca.servo[14].set_pulse_width_range(min_pw, max_pw)
pca.servo[15].set_pulse_width_range(min_pw, max_pw)

pca.servo[0].angle = 0
pca.servo[1].angle = 0
pca.servo[2].angle = 0
pca.servo[3].angle = 0
pca.servo[4].angle = 0
pca.servo[5].angle = 0
pca.servo[6].angle = 0
pca.servo[7].angle = 0
pca.servo[8].angle = 0
pca.servo[9].angle = 0
pca.servo[10].angle = 0
pca.servo[11].angle = 0
pca.servo[12].angle = 0
pca.servo[13].angle = 0
pca.servo[14].angle = 0
pca.servo[15].angle = 0

# 0: Back Left
# 1 : Back Right
# 2 : Front Right
# 3 : Front Center
# 4 : Front Left
# 5 : Right Shoulder
# 6 : Left Shoulder

pca.servo[6].angle = 0
