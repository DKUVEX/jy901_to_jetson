# coding:UTF-8
"""
    test file
"""
import platform
import io
from Dll.lib.Modular.JY901 import JY901
#from Dll.lib.Modular.

welcome = """
Welcome to the WITMOTION sample program
"""

def AppliedCalibration(JY901):
    """
    Addition calibration
    :param JY901: Device model
    :return:
    """
    if JY901.IsOpen():
        # Unlock the register and send the command
        JY901.UnlockReg()
        # Add up calibration
        JY901.AppliedCalibration()

        # The following two lines are equivalent to the above, it is recommended to use the above
        # Unlock the register and send the command
        # JY901.SendProtocolData([0xff, 0xaa, 0x69, 0x88, 0xb5], 50)
        # Add up calibration
        # JY901.SendProtocolData([0xff, 0xaa, 0x01, 0x01, 0x00], 4000)

        print("Completion of total calibration")
    else:
        print("The device is not open")

def StartFieldCalibration(JY901):
    """
    Magnetic Field Calibration
    :param JY901: Device model
    :return:
    """
    if JY901.IsOpen():
        # Unlock the register and send the command
        JY901.UnlockReg()
        # start magnetic field calibration
        JY901.StartFieldCalibration()

        # The following two lines are equivalent to the above, it is recommended to use the above
        # Unlock the register and send the command
        # JY901.SendProtocolData([0xff, 0xaa, 0x69, 0x88, 0xb5], 50)
        # start magnetic field calibration
        # JY901.SendProtocolData([0xff, 0xaa, 0x01, 0x07, 0x00], 100)

        if input("Please make a slow rotation around the XYZ axis respectively, after the three-axis rotation is completed, end the calibration (Y/N)?").lower() == "y":
            # Unlock the register and send the command
            JY901.UnlockReg()
            # end magnetic field calibration
            JY901.EndFieldCalibration()

            # The following two lines are equivalent to the above, it is recommended to use the above
            # Unlock the register and send the command
            # JY901.SendProtocolData([0xff, 0xaa, 0x69, 0x88, 0xb5], 50)
            # start magnetic field calibration
            # JY901.SendProtocolData([0xff, 0xaa, 0x01, 0x00, 0x00], 100)

            print("End magnetic field calibration")
    else:
        print("The device is not open")

def IsReadReg(JY901, reg, waitTime):
    """
    read register
    :param JY901: Device model
    :param reg: register address
    :param waitTime:  wait time
    :return:
    """
    bRet = False
    if JY901.IsOpen():
        # read register
        if JY901.SendReadReg(reg, waitTime):
            bRet = True
        else:
            print(str(reg) + "Failed to read")
    else:
        print("The device is not open")

    return bRet

def JY901_OnRecord(deviceModel):
    """
    This is called when sensor data is refreshed and you can log data here
    :param deviceModel:
    :return:
    """
    builder = io.StringIO()
    # device name
    builder.write(deviceModel.deviceName + "\n")
    # chip time
    builder.write("Chiptime:" + str(deviceModel.GetDeviceData("Chiptime"))+"\t")
    # temperature
    builder.write("Temperature:" + str(deviceModel.GetDeviceData("Temperature"))+"\n")
    # acceleration
    builder.write("AccX:" + str(deviceModel.GetDeviceData("AccX"))+"g \t")
    builder.write("AccY:" + str(deviceModel.GetDeviceData("AccY"))+"g \t")
    builder.write("AccZ:" + str(deviceModel.GetDeviceData("AccZ"))+"g \n")
    # angular velocity
    builder.write("GyroX:" + str(deviceModel.GetDeviceData("GyroX"))+"°/s \t")
    builder.write("GyroY:" + str(deviceModel.GetDeviceData("GyroY"))+"°/s \t")
    builder.write("GyroZ:" + str(deviceModel.GetDeviceData("GyroZ"))+"°/s \n")
    # angle
    builder.write("AngleX:" + str(deviceModel.GetDeviceData("AngleX"))+"° \t")
    builder.write("AngleY:" + str(deviceModel.GetDeviceData("AngleY"))+"° \t")
    builder.write("AngleZ:" + str(deviceModel.GetDeviceData("AngleZ"))+"° \n")
    # Magnetic field
    builder.write("MagX:" + str(deviceModel.GetDeviceData("MagX"))+"uT \t")
    builder.write("MagY:" + str(deviceModel.GetDeviceData("MagY"))+"uT \t")
    builder.write("MagZ:" + str(deviceModel.GetDeviceData("MagZ"))+"uT \n")
    # latitude and longitude
    builder.write("Lon:" + str(deviceModel.GetDeviceData("Lon"))+"\t")
    builder.write("Lat:" + str(deviceModel.GetDeviceData("Lat"))+"\n")
    # barometric pressure and altitude
    builder.write("Pressure:" + str(deviceModel.GetDeviceData("Pressure"))+"\t")
    builder.write("Height:" + str(deviceModel.GetDeviceData("Height"))+"\n")
    # GPS: altitude, heading angle, GPS ground speed
    builder.write("GPSHeight:" + str(deviceModel.GetDeviceData("GPSHeight")) + "\t")
    builder.write("GPSYaw:" + str(deviceModel.GetDeviceData("GPSYaw"))+"\t")
    builder.write("GPSV:" + str(deviceModel.GetDeviceData("GPSV")) + "\n")
    #  Four elements
    builder.write("Q0:" + str(deviceModel.GetDeviceData("Q0"))+"\t")
    builder.write("Q1:" + str(deviceModel.GetDeviceData("Q1"))+"\t")
    builder.write("Q2:" + str(deviceModel.GetDeviceData("Q2"))+"\t")
    builder.write("Q3:" + str(deviceModel.GetDeviceData("Q3"))+"\n")
    #  The port number
    builder.write("D0:" + str(deviceModel.GetDeviceData("D0"))+"\t")
    builder.write("D1:" + str(deviceModel.GetDeviceData("D1"))+"\t")
    builder.write("D2:" + str(deviceModel.GetDeviceData("D2"))+"\t")
    builder.write("D3:" + str(deviceModel.GetDeviceData("D3"))+"\n")
    # Positioning accuracy: number of satellites, position accuracy, horizontal accuracy, vertical accuracy
    builder.write("SVNUM:" + str(deviceModel.GetDeviceData("SVNUM")) + "\t")
    builder.write("PDOP:" + str(deviceModel.GetDeviceData("PDOP"))+"\t")
    builder.write("HDOP:" + str(deviceModel.GetDeviceData("HDOP")) + "\t")
    builder.write("VDOP:" + str(deviceModel.GetDeviceData("VDOP"))+"\n")
    #  version number
    builder.write("VersionNumber:" + str(deviceModel.GetDeviceData("VersionNumber")) + "\n")

    print(builder.getvalue())

if __name__ == '__main__':
    print(welcome)
    # initialize the device
    JY901 = JY901()

    """
    if platform.system().lower() == 'linux':
        PortName = "/dev/ttyUSB0"
    #mac platform name is darwin
    elif platform.system().lower() == 'darwin':
        PortName = "/dev/tty.usbserial-110"
    else:
        PortName = "COM11"
    """

    PortName = input("Enter port ( /dev/ttyTHSx ): ")
    Baudrate = 9600
    # set serial port
    JY901.SetPortName(PortName)
    # set baud rate
    JY901.SetBaudrate(Baudrate)
    # open serial port
    JY901.Open()
    if JY901.IsOpen():
        print("Device opened successfully")

        # Add up calibration
        AppliedCalibration(JY901)

        # Magnetic field calibration
        # StartFieldCalibration(JY901)

        # read 0x03 register
        # wait time
        waitTime = 200
        # Send read command and wait for sensor to return data
        IsReadReg(JY901, 0X03, waitTime)
        #  The following line is equivalent to the above. It is recommended to use the above
        # JY901.SendProtocolData([0xff, 0xaa, 0x27, 0x03, 0x00], waitTime)
        print("0x03 read result:" + str(JY901.GetDeviceData("0x03")))

        # Write the corresponding value of the register: write register 0x03 to 0x06
        JY901.SendWriteReg(0x03, 0x06)
        # save the value of the register
        JY901.SaveReg()
        # The following line is equivalent to the above. It is recommended to use the above
        # JY901.SendProtocolData([0xff, 0xaa, 0x03, 0x06, 0x00], waitTime)
        # save the value of the register
        # JY901.SendProtocolData([0xff, 0xaa, 0x00, 0x00, 0x00], waitTime)

        # Bind receiving events to record data events
        JY901.AddOnRecord(JY901_OnRecord)

        input()

        # close the device
        JY901.Close()
        #  remove event
        JY901.RemoveOnRecord(JY901_OnRecord)
    else:
        print("Failed to open the device")
