from robot.PCA9685 import PCA9685
from time import sleep

modulo = PCA9685()
modulo.init_pca9685()
modulo.set_pwm_freq(50)
modulo.SetEnableOn()
modulo.set_pwm(0, 0, 310)
sleep(1)
modulo.SetEnableOff()

