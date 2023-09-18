""" a test script to emulate a BF-C50 programmer"""
import serial

SERIAL_PORT = "/dev/tty.usbserial-10"

### DATA SENT BY COMPUTER ###

# initial request sent by computer
C_READ_INIT = bytes.fromhex("FE 03 30 08")
# download request?
C_DL_REQ = bytes.fromhex("45 02 50 52 4F 47 52 41 4C")
# ACK
ACK = bytes.fromhex("06")  # ACK byte (sent by computer)

### DATA SENT BY RADIO ###
# expected response to initial program request
R_INIT_RESP = bytes.fromhex("57 03 30 08 1F 03 FF FF FF FF FF FF")


def send_read_init():
    """send the initial program request to the radio"""
    ser.write(C_READ_INIT)
    print("Sent C_READ_INIT data (computer to radio):", C_READ_INIT.hex())


def check_init_resp(received_data):
    """check the response to the initial program request"""
    if received_data == R_INIT_RESP:
        print("Received expected response (radio to computer): ", received_data.hex())
        return True

    print("Received bad init data (radio to computer): %s", received_data.hex())
    return False


if __name__ == "__main__":

    # Setup serial port
    ser = serial.Serial(SERIAL_PORT, baudrate=9600)

    try:
        send_read_init()
        received_data = b""  # Initialize an empty byte string for concatenation
        init_resp = ser.read(12)  # read 12 bytes (len of R_INIT_RESP)
        if check_init_resp(init_resp):
            # send download request?
            ser.write(C_DL_REQ)
            print("Sent C_DL_REQ data (computer to radio):", C_DL_REQ.hex())

        while True:

            print("Waiting for data from radio...")
            # Read data from the serial port in chunks of 4 bytes
            chunk = ser.read(1)
            print("Received data (radio to computer):", chunk.hex())

            # Concatenate the received chunk
            received_data += chunk

            # Check if the first 3 received chunks match R_INIT_RESP
            if len(received_data) == len(R_INIT_RESP):
                if received_data == R_INIT_RESP and not INIT_RESP_RVCD:
                    print(
                        "Received expected response (radio to computer): ",
                        received_data.hex(),
                    )

                else:
                    print("Received data (radio to computer): %s", received_data.hex())

                received_data = b""

    except KeyboardInterrupt:
        print("Exiting tester program.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        ser.close()
