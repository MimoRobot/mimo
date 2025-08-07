import smbus2
from gpiozero import LED
from time import sleep

class PCA9685:
    def __init__(self):
        # Indirizzo I2C del PCA9685 (0x40 è quello di default)
        self.PCA9685_ADDRESS = 0x40
        self.led = LED(5)  # GPIO 5
        # Registri del PCA9685
        self.MODE1 = 0x00
        self.PRESCALE = 0xFE
        self.LED0_ON_L = 0x06

        # Inizializza il bus I2C
        self.bus = smbus2.SMBus(1)

    # Inizializza il PCA9685
    def init_pca9685(self):
        self.bus.write_byte_data(self.PCA9685_ADDRESS, self.MODE1, 0x00)
        self.led.on()
    # Imposta la frequenza PWM
    def set_pwm_freq(self,freq):
        prescale_val = int(round(25000000.0 / (4096.0 * freq)) - 1)
        old_mode = self.bus.read_byte_data(self.PCA9685_ADDRESS, self.MODE1)
        new_mode = (old_mode & 0x7F) | 0x10  # Sleep mode
        self.bus.write_byte_data(self.PCA9685_ADDRESS, self.MODE1, new_mode)
        self.bus.write_byte_data(self.PCA9685_ADDRESS, self.PRESCALE, prescale_val)
        self.bus.write_byte_data(self.PCA9685_ADDRESS, self.MODE1, old_mode)
        sleep(0.005)
        self.bus.write_byte_data(self.PCA9685_ADDRESS, self.MODE1, old_mode | 0x80)
    # Imposta il ciclo di lavoro PWM su un canale specifico
    def set_pwm(self,channel, on, off):
        self.bus.write_byte_data(self.PCA9685_ADDRESS, self.LED0_ON_L + 4*channel, on & 0xFF)
        self.bus.write_byte_data(self.PCA9685_ADDRESS, self.LED0_ON_L + 4*channel + 1, on >> 8)
        self.bus.write_byte_data(self.PCA9685_ADDRESS, self.LED0_ON_L + 4*channel + 2, off & 0xFF)
        self.bus.write_byte_data(self.PCA9685_ADDRESS, self.LED0_ON_L + 4*channel + 3, off >> 8)
    # Attiva Enable
    def SetEnableOn(self):
        self.led.off()
    # Disattiva enable
    def SetEnableOff(self):
        self.led.on()