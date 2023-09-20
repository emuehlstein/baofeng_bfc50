import serial

SERIAL_PORT = "COM1"

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
    "574502501f03ffffffffffffff00010100850100496201007c0100804562500100800008010ec7d2001a28080e002c002cff01ffff403e353254523e3c272653510d0f0b0eff19dd0b23ff87e527182338230003"
)  # a blank default config
R_READ_RESP_WBEEP = bytes.fromhex(
    "574502501f03ffffffffffffff80010100850100496201007c0100804562500100800008750ec7d2021a28080e002c002cff01ffff403e353254523e3c272653510d0f0b0eff19dd0b23ff87e527182338230003"
)


def send_init_resp():
    """Send the response to the initial program request to the computer"""
    ser.write(R_INIT_RESP)
    print("Sent R_INIT_RESP data (radio to computer):", R_INIT_RESP.hex())


def send_read_resp(read_resp):
    """Send the response to the read request to the computer"""
    ser.write(read_resp)
    print("Sent R_READ_RESP data (radio to computer):", read_resp.hex())


if __name__ == "__main__":
    # Setup serial port
    ser = serial.Serial(SERIAL_PORT, baudrate=9600)

    try:
        received_data = b""  # Initialize an empty byte string for concatenation
        while True:
            # Read data from the serial port in chunks of 4 bytes
            chunk = ser.read(1)
            received_data += chunk

            if received_data == C_READ_INIT:
                print("Received C_READ_INIT data (computer to radio):", chunk.hex())
                # clear the buffer
                received_data = b""
                # Send the response to the initial program request
                send_init_resp()

            elif received_data == C_DL_REQ:
                print("Received C_DL_REQ data (computer to radio):", chunk.hex())
                send_read_resp(R_READ_RESP)
            else:
                print("Received unexpected data (computer to radio):", chunk.hex())

    except KeyboardInterrupt:
        print("Exiting fakeradio program.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        ser.close()
