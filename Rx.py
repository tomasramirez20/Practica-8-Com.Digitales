from machine import Pin, SPI, I2C, PWM
import utime, struct
from nrf24l01 import NRF24L01
from ssd1306 import SSD1306_I2C
# ---- OLED ----
i2c = I2C(1, scl=Pin(11), sda=Pin(10), freq=400000)
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)
oled.fill(0)
oled.text("Servo 0-180°", 0, 0)
oled.text("Esperando...", 0, 16)
oled.show()
# ---- Servo con rango completo ----
servo = PWM(Pin(15))
servo.freq(50)

nrf = NRF24L01(spi, csn, ce, payload_size=4)
TX_ADDR = b'\xE1\xF0\xF0\xF0\xF0'
RX_ADDR = b'\xD2\xF0\xF0\xF0\xF0'
nrf.open_tx_pipe(TX_ADDR)
nrf.open_rx_pipe(1, RX_ADDR)
# Configuración IDÉNTICA a TX (2Mbps)
nrf.set_power_speed(0, 2) # 0dBm, 2Mbps
nrf.reg_write(0x01, 0x00)

nrf.reg_write(0x04, 0x00)
nrf.reg_write(0x05, 100) # Canal 100
mover_servo_instantaneo(ultimo_angulo)
def verificar_checksum(sync, angulo, checksum):
calc = (sync + (angulo & 0xFF) + ((angulo >> 8) & 0xFF)) & 0xFF
return checksum == calc
print("📡 RX Servo - 0-180° - 2Mbps - Listo")
# ---- Bucle principal ULTRA RÁPIDO ----
while True:
if nrf.any():
try:
datos = nrf.recv()
sync, angulo, checksum = struct.unpack("<BHB", datos)
(angulo)
contador_paquetes += 1
# Actualizar display solo cada 15 paquetes (no bloquear)
if contador_paquetes >= 15:
oled.fill(0)
oled.text("Servo 0-180°", 0, 0)
oled.text(f"Angulo: {angulo:3d}°", 0, 16)
oled.text("Vel: 2Mbps", 0, 32)
oled.text(f"Pkts: {contador_paquetes}", 0, 48)
oled.show()
print(f"📥RX: {angulo}°")
contador_paquetes = 0
except Exception as e:
print(f"Error: {e}")
# ⚡ Delay mínimo para máxima velocidad
utime.sleep_us(500) # 0.5ms

from machine import Pin, SPI, I2C, PWM
import utime, struct
from nrf24l01 import NRF24L01
from ssd1306 import SSD1306_I2C
oled.text("Servo 0-180°", 0, 0)
oled.text("Esperando...", 0, 16)
oled.show()

# ---- Servo con rango completo ----
servo = PWM(Pin(15))
servo.freq(50)
def mover_servo_instantaneo(angulo):
"""Mueve el servo INSTANTÁNEAMENTE a la posición"""
angulo = max(0, min(180, int(angulo)))
# Conversión directa a pulso PWM
pulso_us = 500 + (angulo * 2000) // 180
servo.duty_ns(pulso_us * 1000)
# ---- Radio MÁXIMA VELOCIDAD ----
spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
csn = Pin(5, Pin.OUT, value=1)
ce = Pin(14, Pin.OUT, value=0)
nrf.open_rx_pipe(1, RX_ADDR)
# Configuración IDÉNTICA a TX (2Mbps)
nrf.set_power_speed(0, 2) # 0dBm, 2Mbps
nrf.reg_write(0x01, 0x00)
nrf.reg_write(0x04, 0x00)
nrf.reg_write(0x05, 100) # Canal 100
nrf.start_listening()
# ---- Variables ----
SYNC_BYTE = 0xA5
ultimo_angulo = 90
ultima_actualizacion = 0
contador_paquetes = 0
mover_servo_instantaneo(ultimo_angulo)
def verificar_checksum(sync, angulo, checksum):
calc = (sync + (angulo & 0xFF) + ((angulo >> 8) & 0xFF)) & 0xFF
return checksum == calc
print("📡 RX Servo - 0-180° - 2Mbps - Listo")
# ---- Bucle principal ULTRA RÁPIDO ----
while True:
):
# ⚡ MOVER SERVO INMEDIATAMENTE
mover_servo_instantaneo(angulo)
contador_paquetes += 1

    
oled.text(f"Pkts: {contador_paquetes}", 0, 48)
oled.show()
print(f"📥RX: {angulo}°")
contador_paquetes = 0
except Exception as e:
print(f"Error: {e}")
# ⚡ Delay mínimo para máxima velocidad
utime.sleep_us(500) # 0.5ms
El servo se mueve a cada posición, pero no se queda quieto porque es
un servo de rotación continua.
En un servo de rotación continua:
• 1500us = STOP (no se mueve)
• <1500us = Gira en una dirección
• >1500us = Gira en la otra dirección