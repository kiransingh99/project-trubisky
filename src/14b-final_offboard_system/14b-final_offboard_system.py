from datetime import datetime # used to give files a unique name
import os.path # for finding relative file path
import serial # for serial port comms
import signal, sys # used to safely exit script

def keyboardInterruptHandler(signal, frame):
    """
    Handler for stopping execution of code via ctrl+C. Ensures open files and
    Serial ports are closed safely. Call this function via the line:
        signal.signal(signal.SIGINT, keyboardInterruptHandler)

    Parameters
    ----------
    signal : enum
        Keyboard input.
    frame : frame
        Current frame.

    Returns
    -------
    None.

    """
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up..."
        .format(signal))
    
    #if file is open, close it
    try:
        f.close()
    except:
        print("No file is open")
    else:
        print("Closing file")

    #if serial port is open, close it
    try:
        serialPort.close()
    except:
        print("Serial port not open")
    else:
        print("Closing serial port")
        
    print("Script terminated successfully")
    sys.exit(0)

def waitForInput():
    """
    Waits for user input to start or restart code. If input is "n", script 
    terminates. If it is anything else, the script (re)starts

    Returns
    -------
    None.

    """
    restart = input("Ready to start?").lower()

    if restart == "n":
        print("Script terminated successfully")
        sys.exit(0)

def openSerial():
    """
    Opens the serial port

    Returns
    -------
    serialPort : serial port object
        This is the object that accesses the serial port throughout the script.
    """
    serialPort = serial.Serial(port = "COM3",
                               baudrate = 9600,
                               bytesize = 8,
                               timeout = 2,
                               stopbits = serial.STOPBITS_ONE)
    return serialPort

def readSerial(serialPort):
    """
    Read contents from the serial port.

    Parameters
    ----------
    serialPort : serial port object
        This is the object that accesses the serial port throughout the script.

    Returns
    -------
    serialString : string
        The contents of one line of serial.

    """
    serialString = ""

    #wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):

        #read data out of the buffer until a new line is found
        serialString = serialPort.readline().decode('Ascii')
        return serialString

def createFile():
    """
    Opens a file for writing. Each file will have a unique name

    Returns
    -------
    f : file object
        The file open for writing.

    """
    #find path to 'data' folder
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "..\\..\\data\\") 
    
    #use current date and time to generate unique file name
    now = datetime.now()
    filename = now.strftime("RAW-%Y.%m.%d-%H.%M.%S")
    
    ext = ".csv"
    
    fullName = path + filename + ext
    f = open(fullName, "w")
    return f

#event handler for if ctrl+c is pressed at any point during the script
signal.signal(signal.SIGINT, keyboardInterruptHandler)

receivingData = False #tracks state of loop below
waitForInput() # wait until user is ready to start script
serialPort = openSerial()

while True:

    # read from serial port if available
    if (serialPort.isOpen()):
        serialString = readSerial(serialPort)
    else:
        print("waiting to open serial port...")

    # if there is content in serialString
    if serialString != None:
        # print(serialString)

        if serialString[0] == "s": # start of file
            # close any file if one already exists
            try:
                f.close()
                print("Starting new file")
            except:
                pass
            f = createFile()
            serialString = serialString[1:] # remove 's' from beginning of string
            receivingData = True
            continue
        elif serialString == "e": # end of transmission
            print("end")
            f.close() # close csv file for writing
            serialPort.close()
            receivingData = False
            break

        # normal data transmission
        if receivingData:
            print(serialString.strip('\n'))
            f.write(serialString.strip('\n')) # write string to file without new line
        else: # if starting flag ('s') has not been read:
            print("Waiting to begin")