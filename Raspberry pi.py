import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_scd4x
import serial
import spidev

# --- Lidar 360 (UART) ---
try:
    # Use the appropriate serial port for your Lidar (e.g., '/dev/ttyS0' or '/dev/ttyUSB0')
    lidar_serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    print("Lidar serial port opened.")
except serial.SerialException as e:
    print(f"Error opening Lidar serial port: {e}")
    lidar_serial = None

def read_lidar_data():
    """Reads and prints raw data from Lidar."""
    if lidar_serial and lidar_serial.in_waiting > 0:
        try:
            # Read a full line of data from the Lidar
            raw_data = lidar_serial.readline().decode('utf-8', errors='ignore').strip()
            if raw_data:
                print(f"Lidar Raw Data: {raw_data}")
        except Exception as e:
            print(f"Lidar data reading error: {e}")
    else:
        print("No Lidar data available.")

# --- PMW3901 (SPI) ---
try:
    spi = spidev.SpiDev()
    spi.open(0, 0) # SPI bus 0, device 0
    spi.max_speed_hz = 1000000
    print("SPI bus for PMW3901 opened.")
except Exception as e:
    print(f"Error opening SPI bus: {e}")
    spi = None

def read_pmw3901():
    """Reads motion data from PMW3901 (simplified)."""
    if spi:
        try:
            # Placeholder: The PMW3901 requires a specific protocol
            # This is not a functional read but demonstrates the SPI command
            spi.xfer2([0x00])
            data = spi.readbytes(10)
            print(f"PMW3901 Data: {data}")
        except Exception as e:
            print(f"PMW3901 SPI communication error: {e}")
    else:
        print("PMW3901 not connected or SPI bus error.")

# --- ADC for MQ-9 and AO-O2 ---
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    adc = ADS.ADS1115(i2c)
    mq9_channel = AnalogIn(adc, ADS.P0)
    aoo2_channel = AnalogIn(adc, ADS.P1)
    print("ADC (ADS1115) connected via I2C.")
except Exception as e:
    print(f"Error connecting to ADC: {e}")
    adc = None

def mq9_ppm(voltage):
    """
    Placeholder function: Convert MQ-9 voltage to estimated ppm.
    This formula needs to be calibrated based on the sensor's datasheet.
    """
    # A proper function would use the Rs/R0 ratio and a calibration curve.
    return voltage * 100

def read_analog_sensors():
    """Reads MQ-9 and AO-O2 voltages and converts to ppm/%."""
    if adc:
        mq9_voltage = mq9_channel.voltage
        aoo2_voltage = aoo2_channel.voltage

        mq9_concentration = mq9_ppm(mq9_voltage)
        oxygen_percentage = (aoo2_voltage / 0.01) * 20.9 # Assumes 10mV output in 20.9% O2

        print(f"MQ-9: {mq9_voltage:.4f} V -> ~{mq9_concentration:.2f} ppm")
        print(f"AO-O2: {aoo2_voltage:.4f} V -> ~{oxygen_percentage:.2f}% O₂")
    else:
        print("ADC not connected, skipping analog sensor readings.")

# --- SCD40 (I2C) ---
try:
    scd40 = adafruit_scd4x.SCD4X(i2c)
    print("SCD40 sensor found and connected.")
except Exception as e:
    print(f"Error connecting to SCD40: {e}")
    scd40 = None

def setup_scd40():
    """Initializes SCD40 sensor."""
    if scd40:
        try:
            scd40.start_periodic_measurement()
            print("SCD40: Measurement started.")
        except Exception as e:
            print(f"SCD40 setup error: {e}")

def read_scd40():
    """Reads CO₂, temperature, humidity from SCD40."""
    if scd40:
        try:
            if scd40.data_ready:
                print(f"CO₂: {scd40.CO2} ppm | Temp: {scd40.temperature:.2f} °C | Humidity: {scd40.relative_humidity:.2f}%")
            else:
                print("SCD40 data not ready.")
        except Exception as e:
            print(f"SCD40 read error: {e}")
    else:
        print("SCD40 not connected, skipping readings.")

# --- Main Loop ---
if __name__ == "__main__":
    print("Initializing sensors...")
    time.sleep(5) # Stabilization delay
    setup_scd40()

    try:
        while True:
            print("\n--- Sensor Readings ---")
            read_lidar_data()
            read_pmw3901()
            read_analog_sensors()
            read_scd40()
            print("------------------------")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nExiting gracefully. Goodbye!")
    finally:
        # Close serial and SPI connections
        if lidar_serial:
            lidar_serial.close()
            print("Lidar serial port closed.")
        if spi:
            spi.close()
            print("SPI bus closed.")