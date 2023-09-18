""" a test script to emulate a BF-C50 programmer"""
import serial

SERIAL_PORT = "/dev/tty.usbserial-110"

### DATA SENT BY COMPUTER ###

# initial request sent by computer
C_READ_INIT = bytes.fromhex("FE 03 30 08")
# download request?
C_DL_REQ = bytes.fromhex("45 02 50 52 4F 47 52 41 4C")
ACK = bytes.fromhex("02")

### DATA SENT BY RADIO ###
# expected response to initial program request
R_INIT_RESP = bytes.fromhex("57 03 30 08 1F 03 FF FF FF FF FF FF")
R_READ_RESP = bytes.fromhex(
    "574502501f03ffffffffffffffff010100850100496201007c0100804562500100800008019d8392021a28080e002c002cff01ffff403e353254523e3c272653510d0f0b0eff19dd0a23ff87e527182d3b230003"
)


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


def check_read_resp(read_resp):
    """check the response to the read request"""
    if read_resp == R_READ_RESP:
        print("Received expected response (radio to computer): ", read_resp.hex())
        return True

    print("Received bad read data (radio to computer): %s", read_resp.hex())
    return False


if __name__ == "__main__":

    # Setup serial port
    ser = serial.Serial(SERIAL_PORT, baudrate=9600)

    try:
        send_read_init()
        received_data = b""  # Initialize an empty byte string for concatenation
        init_resp = ser.read(12)  # read 12 bytes (len of R_INIT_RESP)
        if check_init_resp(init_resp):
            # send ACK
            ser.write(ACK)
            print("Sent ACK data (computer to radio):", ACK.hex())

            # send download request?
            ser.write(C_DL_REQ)
            print("Sent C_DL_REQ data (computer to radio):", C_DL_REQ.hex())

        while True:

            # print("Waiting for data from radio...")
            # Read data from the serial port in chunks of 4 bytes
            chunk = ser.read(1)
            # print("Received data (radio to computer):", chunk.hex())

            # Concatenate the received chunk
            received_data += chunk

            if len(received_data) == 84:
                check_read_resp(received_data)

    except KeyboardInterrupt:
        print("Exiting tester program.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        print("Received final data: ", received_data.hex())
        print("Total length of received data:", len(received_data))
        ser.close()
