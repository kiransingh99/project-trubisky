import sys
import serial
from datetime import datetime

def waitForInput():
    restart = input("Ready to start?").lower()

    if restart == "n":
        sys.exit("Script terminated successfully")

def openSerial():
    serialPort = serial.Serial(port = "COM4",
                               baudrate = 9600,
                               bytesize = 8,
                               timeout = 2,
                               stopbits = serial.STOPBITS_ONE)
    return serialPort

def readSerial(serialPort):
    serialString = ""

    #wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):

        #read data out of the buffer until a new line is found
        serialString = serialPort.readline().decode('Ascii')
        return serialString;

def createFile():
    path = "..\\data\\"
    ext = ".csv"
    now = datetime.now()
    filename = now.strftime("RAW-%Y.%m.%d-%H.%M.%S")
    fullName = path + filename + ext
    f = open(fullName, "w")
    return f

receivingData = False
waitForInput();
serialPort = openSerial()

while True:

    if (serialPort.isOpen()):
        serialString = readSerial(serialPort)
    """else:
        print("waiting to open serial port...")"""

    if serialString != None:
        print(serialString)
        """
        if "init" in serialString: #start of transmission
            if not receivingData:
                print("init")
                f = createFile()
                receivingData = True
        elif "end" in serialString: #end of transmission
            if receivingData:
                print("end")
                f.close() #close csv file for writing
                serialPort.close()
                waitForInput() #don't open serial/new file until ready
                receivingData = False
                serialPort = openSerial() #open serialPort here to ensure port is already closed

        else: #normal data transmission
            if receivingData:
                print(serialString)
                f.write(serialString)
            else:
                print("Waiting to begin...")"""