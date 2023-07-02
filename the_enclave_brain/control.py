import ctypes
import glob
import struct
import serial
import sys

ser = None

RGB_struct_format = "BBBB"  # 4 uint8 for lightIdx, R, G, and B values
class RGB(ctypes.Structure):
    _fields_ = [
        ("lightIdx", ctypes.c_ubyte),
        ("R", ctypes.c_ubyte),
        ("G", ctypes.c_ubyte),
        ("B", ctypes.c_ubyte)
    ]

ctrl_input_format = "bBH" # char, uint8, uint16
class ctrl_input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_char), # b for button, p for pot
        ("idx", ctypes.c_ubyte), # which button/pot (1-3)
        ("val", ctypes.c_uint16), # 1 or 0 for button, 0-65535 for pot
    ]

def get_serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.usbmodem*')
    else:
        raise EnvironmentError('Unsupported platform')

    return ports

def init_uc_comms():
    global ser
    ports = get_serial_ports()
    print("Available serial ports", ports)
    try:
        ser = serial.Serial(
            port=ports[0],
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        print("Successfully connected to micro controller")
    except Exception as e:
        print("Failed to connect to micro controller:", e)

# Led idx is 0 or 1 cause we have two floodlights
def tx_floodlight_packet(led_idx, R, G, B):
    rgb_value = RGB(lightIdx=led_idx, R=R, G=G, B=B)
    packed_data = struct.pack(RGB_struct_format, rgb_value.lightIdx, rgb_value.R, rgb_value.G, rgb_value.B)
    
    # transmit it to uC
    if ser is not None:
        ser.write(packed_data)

# Do this while returned value is not none 
def rx_uc_packet():
    if ser is not None:
        if ser.in_waiting > 0:
            packed_rx_data = ser.read(struct.calcsize(ctrl_input_format))
            unpacked_data = struct.unpack(ctrl_input_format, packed_rx_data)
            ctrl_type, ctrl_idx, ctrl_val = unpacked_data
            new_ctrl_input = ctrl_input(type=ctrl_type, idx=ctrl_idx, val=ctrl_val)

            # Handle data
            # print("\nReceived data", new_ctrl_input.type, new_ctrl_input.idx, new_ctrl_input.val)
            return(new_ctrl_input.type, new_ctrl_input.idx, float(new_ctrl_input.val) / 4094.0)
        else:
            return None
    # else:
    #     print('start microcontroller first')


# WORKING EXAMPLE

# def main():
#     # Test COM port
#     ser = serial.Serial(
#         port='COM4', # For mac, '/dev/tty.usbserial' or '/dev/tty0'
#         baudrate=115200,
#         bytesize=serial.EIGHTBITS,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE
#     )

#     while True:

#         # Create an instance of the RGB structure
#         rgb_value = RGB(1, 255, 128, 0)
#         packed_data = struct.pack(RGB_struct_format, rgb_value.lightIdx, rgb_value.R, rgb_value.G, rgb_value.B)
        
#         # transmit it to uC
#         ser.write(packed_data)

#         # Rx from uC
#         while ser.in_waiting > 0:
#             packed_rx_data = ser.read(struct.calcsize(ctrl_input_format))
#             unpacked_data = struct.unpack(ctrl_input_format, packed_rx_data)
#             new_ctrl_input = ctrl_input(*unpacked_data)

#             # Handle data
#             print(new_ctrl_input.type, new_ctrl_input.idx, new_ctrl_input.val)

#         time.sleep(1)
