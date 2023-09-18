import serial

# Define the c_read_init data (sent by computer) and ACK byte using .fromhex()
c_read_init = bytes.fromhex("FE 03 30 08")
r_init_resp = bytes.fromhex("57 03 30 08 1F 03 FF FF FF FF FF FF")  # r_ prefix for data sent by the radio
ack = bytes.fromhex("06")  # ACK byte (sent by computer)

# Serial port settings
ser = serial.Serial('/dev/tty.usbserial-10', baudrate=9600)

try:
    # Send the c_read_init data
    ser.write(c_read_init)
    print("Sent c_read_init data (computer to radio):", c_read_init.hex())

    while True:
        # Wait for a response and print it in hex
        received_data = ser.read(len(r_init_resp))
        print("Received data (radio to computer):", received_data.hex())

        if received_data == r_init_resp:
            print("Received expected response (radio to computer).")
            
            # Send an ACK (computer to radio)
            ser.write(ack)
            print("Sent ACK (computer to radio):", ack.hex())
        else:
            print("Received unexpected response (radio to computer).")
        
        # Continue listening for more data
except KeyboardInterrupt:
    print("Exiting program.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    ser.close()

