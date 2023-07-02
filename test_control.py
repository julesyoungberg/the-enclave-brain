import ctypes
import struct
import time
import serial

RGB_struct_format = "BBBB"  # 4 uint8 for lightIdx, R, G, and B values
class RGB(ctypes.Structure):
    fields = [
        ("lightIdx", ctypes.c_ubyte),
        ("R", ctypes.c_ubyte),
        ("G", ctypes.c_ubyte),
        ("B", ctypes.c_ubyte)
    ]

ctrl_input_format = "bBH" # char, uint8, uint16
class ctrl_input(ctypes.Structure):
    fields = [
        ("type", ctypes.c_char), # b for button, p for pot
        ("idx", ctypes.c_ubyte), # which button/pot (1-3)
        ("val", ctypes.c_uint16), # 1 or 0 for button, 0-65535 for pot
    ]

def main():
    # Test COM port
    ser = serial.Serial(
        port='/dev/tty.usbmodem11103', # For mac, '/dev/tty.usbserial' or '/dev/tty0'
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE
    )

    while True:

        # Create an instance of the RGB structure
        rgb_value = RGB(lightIdx=1, R=255, G=128, B=255)
        packed_data = struct.pack(RGB_struct_format, rgb_value.lightIdx, rgb_value.R, rgb_value.G, rgb_value.B)
        
        # transmit it to uC
        ser.write(packed_data)

        # Rx from uC
        while ser.in_waiting > 0:
            packed_rx_data = ser.read(struct.calcsize(ctrl_input_format))
            unpacked_data = struct.unpack(ctrl_input_format, packed_rx_data)
            ctrl_type, ctrl_idx, ctrl_val = unpacked_data
            new_ctrl_input = ctrl_input(type=ctrl_type, idx=ctrl_idx, val=ctrl_val)

            # Handle data
            print(new_ctrl_input.type, new_ctrl_input.idx, new_ctrl_input.val)

        time.sleep(1)


if __name__ == "__main__":
    main()