from machine import I2C, Pin
import time

# DRV2605L Registers
DRV2605L_ADDR = 0x5A
DRV2605L_MODE = 0x01
DRV2605L_GO = 0x0C
DRV2605L_WAVESEQ1 = 0x04
DRV2605L_OVERDRIVE_CLAMP = 0x17
DRV2605L_RATED_VOLTAGE = 0x16
DRV2605L_LIBRARY = 0x03
DRV2605L_FEEDBACK = 0x1A
DRV2605L_CONTROL1 = 0x1B
DRV2605L_CONTROL2 = 0x1C
DRV2605L_CONTROL3 = 0x1D

class DRV2605L:
    def __init__(self, i2c, address=DRV2605L_ADDR):
        self.i2c = i2c
        self.address = address
        self.init()

    def init(self):
        # Set to internal trigger mode
        self.write_register(DRV2605L_MODE, 0x00)
        self.configure_feedback()  # Configure feedback settings
        self.configure_control()   # Configure control registers

    def configure_feedback(self, use_erm=True):
        """Configure the feedback register."""
        feedback = self.read_register(DRV2605L_FEEDBACK)
        if use_erm:
            feedback &= ~0x80  # Clear bit 7 for ERM
        else:
            feedback |= 0x80  # Set bit 7 for LRA
        self.write_register(DRV2605L_FEEDBACK, feedback)

    def configure_control(self):
        """Configure advanced control registers."""
        self.write_register(DRV2605L_CONTROL1, 0x93)  # Example: Setting gain and filters
        self.write_register(DRV2605L_CONTROL2, 0xF5)  # Example: Advanced timing control
        self.write_register(DRV2605L_CONTROL3, 0xA0)  # Example: Enable ERM open-loop

    def select_library(self, library_id):
        self.write_register(DRV2605L_LIBRARY, library_id)

    def set_waveform(self, slot, effect):
        self.write_register(DRV2605L_WAVESEQ1 + slot, effect)

    def go(self):
        self.write_register(DRV2605L_GO, 0x01)

    def stop(self):
        self.set_waveform(0, 0)  # Clear waveforms
        self.go()  # Trigger with no effect to stop

    def set_voltage(self, rated_voltage, overdrive_clamp):
        self.write_register(DRV2605L_RATED_VOLTAGE, rated_voltage)
        self.write_register(DRV2605L_OVERDRIVE_CLAMP, overdrive_clamp)

    def write_register(self, reg, value):
        self.i2c.writeto_mem(self.address, reg, bytearray([value]))

    def read_register(self, reg):
        return self.i2c.readfrom_mem(self.address, reg, 1)[0]

# Initialize I2C
i2c = I2C(0, scl=Pin(13), sda=Pin(12))  # Use appropriate pins for your board, e.g. RP2040 (Pico)
drv = DRV2605L(i2c)

# Example usage
print("Initializing DRV2605L...")
drv.set_voltage(0x80, 0x90)  # Set voltage for 3.3V operation 
drv.select_library(1)        # Use ERM library

# Example: Ramp Effect
print("Playing ramp effect...")
drv.set_waveform(0, 47)  # Increment effect
drv.set_waveform(1, 48)  # Decrement effect
drv.set_waveform(2, 0)   # End sequence
drv.go()
time.sleep(1)  # Vibrates for 1 second
drv.stop()
print("Ramp effect completed.")

