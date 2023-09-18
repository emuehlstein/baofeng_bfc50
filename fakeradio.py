import serial

# Define the expected c_read_init data (sent by computer) and ACK byte using .fromhex()
c_read_init = bytes.fromhex("FE 03 30 08")  # Expected data sent by computer
ack = bytes.fromhex("06")  # ACK byte (sent by radio to acknowledge)

# Define the response r_init_resp data (sent by radio) using .fromhex()
r_init_resp = bytes.fromhex("57 03 30 08 1F 03 FF FF FF FF FF FF")

# Serial port settings
ser = serial.Serial('/dev/tty.usbserial-10', baudrate=9600)

try:
    while True:
        # Wait for the c_read_init data and print it in hex
        received_data = ser.read(len(c_read_init))
        print("Received data (computer to radio):", received_data.hex())

        if received_data == c_read_init:
            print("Received c_read_init data (computer to radio).")
            
            # Send the r_init_resp data (radio to computer)
            ser.write(r_init_resp)
            print("Sent r_init_resp data (radio to computer):", r_init_resp.hex())
            
            # Wait for the ACK from the computer
            ack_data = ser.read(len(ack))
            print("Received ACK (computer to radio):", ack_data.hex())
        else:
            print("Received unexpected data (computer to radio).")
        
        # Continue listening for more data
except KeyboardInterrupt:
    print("Exiting program.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    ser.close()

