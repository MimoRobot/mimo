from RPLCD.i2c import CharLCD
from time import sleep

# Sostituisci 0x27 con l’indirizzo I2C corretto
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=20, rows=4, dotsize=8,
              charmap='A00', auto_linebreaks=True)

# Scrivi qualcosa sul display
lcd.clear()
lcd.write_string('Ciao Umberto!')

# Vai alla seconda riga
lcd.cursor_pos = (1, 0)
lcd.write_string('Display 20x4')

# Terza riga
lcd.cursor_pos = (2, 0)
lcd.write_string('Funziona bene!')
# Quarta riga
lcd.cursor_pos = (3, 0)
lcd.write_string('ARRIVERDERCI')

sleep(5)
lcd.clear()
