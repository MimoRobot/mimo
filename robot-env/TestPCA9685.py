import smbus2
import RPi.GPIO as GPIO
import time

# Indirizzo I2C del PCA9685 (0x40 è quello di default)
PCA9685_ADDRESS = 0x40
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(5, GPIO.OUT)
# Registri del PCA9685
MODE1 = 0x00
PRESCALE = 0xFE
LED0_ON_L = 0x06

# Inizializza il bus I2C
bus = smbus2.SMBus(1)

# Inizializza il PCA9685
def init_pca9685():
    bus.write_byte_data(PCA9685_ADDRESS, MODE1, 0x00)

# Imposta la frequenza PWM
def set_pwm_freq(freq):
    prescale_val = int(round(25000000.0 / (4096.0 * freq)) - 1)
    old_mode = bus.read_byte_data(PCA9685_ADDRESS, MODE1)
    new_mode = (old_mode & 0x7F) | 0x10  # Sleep mode
    bus.write_byte_data(PCA9685_ADDRESS, MODE1, new_mode)
    bus.write_byte_data(PCA9685_ADDRESS, PRESCALE, prescale_val)
    bus.write_byte_data(PCA9685_ADDRESS, MODE1, old_mode)
    time.sleep(0.005)
    bus.write_byte_data(PCA9685_ADDRESS, MODE1, old_mode | 0x80)

# Imposta il ciclo di lavoro PWM su un canale specifico
def set_pwm(channel, on, off):
    bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L + 4*channel, on & 0xFF)
    bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L + 4*channel + 1, on >> 8)
    bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L + 4*channel + 2, off & 0xFF)
    bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L + 4*channel + 3, off >> 8)

# Inizializza il PCA9685
init_pca9685()

# Imposta la frequenza a 50Hz per il controllo dei servo
set_pwm_freq(50)
GPIO.output(5, GPIO.LOW)
#GPIO.output(4, GPIO.HIGH)
try:
    while True:
        set_pwm(0, 0,360)  # Imposta il servo a una posizione
        time.sleep(2)
        set_pwm(1, 0, 300)  # Imposta il servo a un'altra posizione
        time.sleep(2)
       
except KeyboardInterrupt:
    # Pulisci i settaggi dei GPIO quando si interrompe il programma
    GPIO.cleanup()