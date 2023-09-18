# tester.py

import serial

INIT_RESP_RVCD = False  # Flag to indicate if the initial response has been received

# Define the  data (sent by computer) and ACK byte using .fromhex()
c_read_init = bytes.fromhex("FE 03 30 08")
c_dl_req = bytes.fromhex("45 02 50 52 4F 47 52 41 4C")  # download request? data sent by computer
ack = bytes.fromhex("06")  # ACK byte (sent by computer)

# Define the expected response (sent by radio) using .fromhex()
r_init_resp = bytes.fromhex("57 03 30 08 1F 03 FF FF FF FF FF FF")  # expected response to initial program request

# Serial port settings
ser = serial.Serial('/dev/tty.usbserial-10', baudrate=9600)

try:
    # Send the c_read_init data
    ser.write(c_read_init)
    print("Sent c_read_init data (computer to radio):", c_read_init.hex())

    received_data = b""  # Initialize an empty byte string for concatenation

    while True:
        # Read data from the serial port in chunks of 4 bytes
        chunk = ser.read(1)
        # print("Received data (radio to computer):", chunk.hex())

        # Concatenate the received chunk
        received_data += chunk

        # Check if the first 3 received chunks match r_init_resp
        if len(received_data) == len(r_init_resp):
            if received_data == r_init_resp and not INIT_RESP_RVCD:
                print("Received expected response (radio to computer): ", received_data.hex())
                
                
                
                # flag the initial response as received
                INIT_RESP_RVCD = True
                
                # Send an ACK (computer to radio)
       
                ser.write(ack)
                print("Sent ACK (computer to radio):", ack.hex())
                
                # send download request?
                ser.write(c_dl_req)
                print("Sent c_dl_req data (computer to radio):", c_dl_req.hex())

            else:
                print("Received data (radio to computer): %s",received_data.hex() )
    

            received_data = b""
        
        # Continue listening for more data
except KeyboardInterrupt:
    print("Exiting tester program.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    ser.close()
