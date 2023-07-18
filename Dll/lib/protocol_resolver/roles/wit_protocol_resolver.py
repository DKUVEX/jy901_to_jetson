# coding:UTF-8
import time
from Dll.lib.protocol_resolver.interface.i_protocol_resolver import IProtocolResolver


class WitProtocolResolver(IProtocolResolver):
    TempBytes = []          # Temporary data list
    PackSize = 11           # Size of a data packet
    gyroRange = 2000.0      # Gyroscopic range
    accRange = 16.0         # Accelerometer range
    angleRange = 180.0      # Angle range
    TempFindValues = []     # Data returned from reading a certain register
    isFirst = True
    iFindStartReg = -1      # First register being read

    FIXED_HEADER_BYTES = [0xff, 0xaa]

    def setConfig(self, deviceModel):
        pass

    def sendData(self, sendData, deviceModel):
        if len(sendData) > 4:
            if sendData[0] == 0xff and sendData[1] == 0xaa and sendData[2] == 0x27:
                self.iFindStartReg = sendData[3]
        success_bytes = deviceModel.serialPort.write(sendData)
        
    def passiveReceiveData(self, data, deviceModel):
        """
        receive and process data
        :param data: serial data
        :param deviceModel: device model
        :return:
        """
        global TempBytes
        for val in data:
            self.TempBytes.append(val)
            if self.TempBytes and self.TempBytes[0] != 0x55:    #check if TempBytes is not empty and first element is not 0x55
                del self.TempBytes[0]                           #remove first byte and continue
                continue


            if len(self.TempBytes) > 1 and not (0x50 <= self.TempBytes[1] <= 0x5a) and self.TempBytes[1] != 0x5f:
                # if (((self.TempBytes[1] - 0x50 >= 0 and self.TempBytes[1] - 0x50 <= 11) or self.TempBytes[1]==0x5f) == False):   #第二个字节数值不在0x50~0x5a范围或者不等于0x5f
                #     del self.TempBytes[0]           
                #     continue
                del self.TempBytes[0]
                continue
            
            if len(self.TempBytes) == self.PackSize:      #check if we have the required pack size
                CheckSum = 0                                #initialize check sum
                for i in range(self.PackSize-1):
                    CheckSum += self.TempBytes[i]

                if CheckSum & 0xff == self.TempBytes[self.PackSize-1]:  #chekcsum verification passed
                    #mapping the packet type to the corresponding method to avoid too many if statements
                    packet_types = {
                        0x50: self.get_chiptime,
                        0x51: self.get_acc,
                        0x52: self.get_gyro,
                        0x53: self.get_angle,
                        0x54: self.get_mag,
                        0x55: self.get_port,
                        0x56: self.get_pressureHeight,
                        0x57: self.get_lonlat,
                        0x58: self.get_gps,
                        0x59: self.get_four_elements,
                        0x5a: self.get_positioning_accuracy,
                        0x5b: self.get_find
                    }
                    packet_type = self.TempBytes[1]
                    if packet_type in packet_types:
                        #handle the cases for packet_type 0x51
                        if packet_type == 0x51: 
                            if self.isFirst == False: #check if first time processing acc
                                deviceModel.dataProcessor.onUpdate(deviceModel)
                            else:
                                self.isFirst = False
                            self.get_acc(self.TempBytes, deviceModel)
                        #fetch packet type and call the appropriate function
                        packet_types[packet_type](self.TempBytes, deviceModel)   
                    self.TempBytes = [] #reset data dump


                    # if self.TempBytes[1] == 0x50:                      #芯片时间包
                    #     self.get_chiptime(self.TempBytes, deviceModel) #结算芯片时间数据
                    # elif self.TempBytes[1] == 0x51:                    #加速度包
                    #     if self.isFirst == False:
                    #         deviceModel.dataProcessor.onUpdate(deviceModel)  # 触发数据更新事件
                    #     else:
                    #         self.isFirst = False
                    #     self.get_acc(self.TempBytes, deviceModel)      #结算加速度数据
                    # elif self.TempBytes[1] == 0x52:                    #角速度包
                    #     self.get_gyro(self.TempBytes, deviceModel)     #结算角速度数据
                    # elif self.TempBytes[1] == 0x53:                    #角度包
                    #     self.get_angle(self.TempBytes, deviceModel)    #结算角度数据
                    # elif self.TempBytes[1] == 0x54:                    #磁场包
                    #     self.get_mag(self.TempBytes, deviceModel)     #结算磁场数据
                    # elif self.TempBytes[1] == 0x55:                    #端口包
                    #     self.get_port(self.TempBytes, deviceModel)     #结算端口数据
                    # elif self.TempBytes[1] == 0x56:                    #气压和高度包
                    #     self.get_pressureHeight(self.TempBytes, deviceModel)     #结算气压和高度数据
                    # elif self.TempBytes[1] == 0x57:                    #经纬度包
                    #     self.get_lonlat(self.TempBytes, deviceModel)     #结算经纬度数据
                    # elif self.TempBytes[1] == 0x58:                    #gps包
                    #     self.get_gps(self.TempBytes, deviceModel)     #结算gps数据
                    # elif self.TempBytes[1] == 0x59:                    #四元素包
                    #     self.get_four_elements(self.TempBytes, deviceModel)     #结算四元素数据
                    # elif self.TempBytes[1] == 0x5a:                    #定位精度包
                    #     self.get_positioning_accuracy(self.TempBytes, deviceModel)     #结算定位精度数据
                    # elif self.TempBytes[1] == 0x5f:           #返回读取指定的寄存器
                    #     self.get_find(self.TempBytes, deviceModel)
                    # self.TempBytes = []                        #清除数据
                else:                                        #校验和未通过
                    del self.TempBytes[0]                    # 去除第一个字节

    def get_readbytes(self, regAddr):
        """
        read bytes from resgiter adress
        :param regAddr: register adress
        :return:
        """
        low_byte = regAddr & 0xff
        high_byte = regAddr >> 8
        return self.FIXED_HEADER_BYTES + [0x27, low_byte, high_byte]
        #return [0xff, 0xaa, 0x27, regAddr & 0xff, regAddr >> 8]

    def get_writebytes(self, regAddr, sValue):
        """
        write bytes
        :param regAddr: register adress
        :param sValue: register value
        :return:
        """
        low_byte = sValue & 0xff
        high_byte = sValue >> 8
        return self.FIXED_HEADER_BYTES + [regAddr, low_byte, high_byte]
        #return [0xff, 0xaa, regAddr, sValue & 0xff, sValue >> 8]

    def get_acc(self, datahex, deviceModel):
        """
        get accelaration
        :param datahex: input data
        :param deviceModel: device model
        :return:
        """
        axl = datahex[2]
        axh = datahex[3]
        ayl = datahex[4]
        ayh = datahex[5]
        azl = datahex[6]
        azh = datahex[7]

        
        acc_x = (axh << 8 | axl) / 32768.0 * self.accRange
        acc_y = (ayh << 8 | ayl) / 32768.0 * self.accRange
        acc_z = (azh << 8 | azl) / 32768.0 * self.accRange


        # if acc_x >= self.accRange:
        #     acc_x -= 2 * self.accRange
        # if acc_y >= self.accRange:
        #     acc_y -= 2 * self.accRange
        # if acc_z >= self.accRange:
        #     acc_z -= 2 * self.accRange

        #acceleration range correction if acc more than range else dont change
        acc_x -= -2 * self.accRange if acc_x >= self.accRange else 0
        acc_y -= -2 * self.accRange if acc_y >= self.accRange else 0
        acc_z -= -2 * self.accRange if acc_z >= self.accRange else 0

        deviceModel.setDeviceData("AccX", round(acc_x, 4))
        deviceModel.setDeviceData("AccY", round(acc_y, 4))   
        deviceModel.setDeviceData("AccZ", round(acc_z, 4))     

        # calculate temperature and set it to the device
        tempVal = (datahex[9] << 8 | datahex[8])
        Temperature = round(tempVal / 100.0, 2)                             
        deviceModel.setDeviceData("Temperature", Temperature)                             

    def get_gyro(self, datahex, deviceModel):
        """
        get gyro data
        :param datahex: hex data input
        :param deviceModel: device model
        :return:
        """
        wxl = datahex[2]
        wxh = datahex[3]
        wyl = datahex[4]
        wyh = datahex[5]
        wzl = datahex[6]
        wzh = datahex[7]

        gyro_x = (wxh << 8 | wxl) / 32768.0 * self.gyroRange
        gyro_y = (wyh << 8 | wyl) / 32768.0 * self.gyroRange
        gyro_z = (wzh << 8 | wzl) / 32768.0 * self.gyroRange

        # if gyro_x >= self.gyroRange:
        #     gyro_x -= 2 * self.gyroRange
        # if gyro_y >= self.gyroRange:
        #     gyro_y -= 2 * self.gyroRange
        # if gyro_z >= self.gyroRange:
        #     gyro_z -= 2 * self.gyroRange

        gyro_x -= -2 * self.gyroRange if gyro_x >= self.gyroRange else 0
        gyro_y -= -2 * self.gyroRange if gyro_y >= self.gyroRange else 0
        gyro_z -= -2 * self.gyroRange if gyro_z >= self.gyroRange else 0

        #assign values to device
        deviceModel.setDeviceData("GyroX", round(gyro_x, 4))  
        deviceModel.setDeviceData("GyroY", round(gyro_y, 4))   
        deviceModel.setDeviceData("GyroZ", round(gyro_z, 4))   

    def get_angle(self, datahex, deviceModel):
        """
        角度结算
        :param datahex: 原始始数据包
        :param deviceModel: 设备模型
        :return:
        """
        rxl = datahex[2]
        rxh = datahex[3]
        ryl = datahex[4]
        ryh = datahex[5]
        rzl = datahex[6]
        rzh = datahex[7]

        

        angle_x = (rxh << 8 | rxl) / 32768.0 * self.angleRange
        angle_y = (ryh << 8 | ryl) / 32768.0 * self.angleRange
        angle_z = (rzh << 8 | rzl) / 32768.0 * self.angleRange

        # if angle_x >= self.angleRange:
        #     angle_x -= 2 * self.angleRange
        # if angle_y >= self.angleRange:
        #     angle_y -= 2 * self.angleRange
        # if angle_z >= self.angleRange:
        #     angle_z -= 2 * self.angleRange

        angle_x -= -2 * self.angleRange if angle_x >= self.angleRange else 0
        angle_y -= -2 * self.angleRange if angle_y >= self.angleRange else 0
        angle_z -= -2 * self.angleRange if angle_z >= self.angleRange else 0

        deviceModel.setDeviceData("AngleX", round(angle_x, 3))  # 设备模型角度X赋值
        deviceModel.setDeviceData("AngleY", round(angle_y, 3))  # 设备模型角度Y赋值
        deviceModel.setDeviceData("AngleZ", round(angle_z, 3))  # 设备模型角度Z赋值

        #set version number
        #Version = deviceModel.get_int(bytes([datahex[8], datahex[9]]))
        deviceModel.setDeviceData("VersionNumber", deviceModel.get_int(bytes([datahex[8], datahex[9]])))

    def get_mag(self, datahex, deviceModel):
        """
        get magnetic field data
        :param datahex: hex data input
        :param deviceModel: device model
        :return:
        """

        #TODO: no need for calling the deviceModel.get_int method and direclty extracting int value here using
        #      builtin function?
        _x = deviceModel.get_int(bytes([datahex[2], datahex[3]]))
        _y = deviceModel.get_int(bytes([datahex[4], datahex[5]]))
        _z = deviceModel.get_int(bytes([datahex[6], datahex[7]]))

        deviceModel.setDeviceData("MagX", round(_x, 0))
        deviceModel.setDeviceData("MagY", round(_y, 0))
        deviceModel.setDeviceData("MagZ", round(_z, 0))

    def get_port(self, datahex, deviceModel):
        """
        get port info
        :param datahex: hex input data
        :param deviceModel: device model
        :return:
        """
        D0 = deviceModel.get_int(bytes([datahex[2], datahex[3]]))
        D1 = deviceModel.get_int(bytes([datahex[4], datahex[5]]))
        D2 = deviceModel.get_int(bytes([datahex[6], datahex[7]]))
        D3 = deviceModel.get_int(bytes([datahex[8], datahex[9]]))

        # set port info to device
        deviceModel.setDeviceData("D0", round(D0, 0))
        deviceModel.setDeviceData("D1", round(D1, 0))
        deviceModel.setDeviceData("D2", round(D2, 0))
        deviceModel.setDeviceData("D3", round(D3, 0))

    def get_lonlat(self, datahex, deviceModel):
        """
        get longitude and latitude data
        :param datahex: hex input data
        :param deviceModel: device model
        :return:
        """

        # lon = deviceModel.get_unint(bytes([datahex[2], datahex[3], datahex[4], datahex[5]]))
        # lat = deviceModel.get_unint(bytes([datahex[6], datahex[7], datahex[8], datahex[9]]))

        lon = datahex[5] << 24 | datahex[4] << 16 << datahex[3] << 8 | datahex[2]
        lat = datahex[9] << 24 | datahex[8] << 16 << datahex[7] << 8 | datahex[6]

        #(lon / 10000000 + ((double)(lon % 10000000) / 1e5 / 60.0)).ToString("f8")
        # tlon = lon / 10000000.0
        # tlat = lat / 10000000.0

        deviceModel.setDeviceData("Lon", round(lon / 10000000.0, 8))
        deviceModel.setDeviceData("Lat", round(lat / 10000000.0, 8))

    def get_pressureHeight(self, datahex, deviceModel):
        """
        get pressure and height data
        :param datahex: hex input data
        :param deviceModel: device model
        :return:
        """

        # Pressure = deviceModel.get_unint(bytes([datahex[2], datahex[3], datahex[4], datahex[5]]))
        # Height = deviceModel.get_unint(bytes([datahex[6], datahex[7], datahex[8], datahex[9]])) / 100.0

        # using direclty bitwise operation to extract necessary data and calculate the values as per documentation
        # no need for @device.get_unint?
        Pressure = ((datahex[5] << 24) | (datahex[4] << 16) | (datahex[3] << 8) | datahex[2])
        Height = ((datahex[9] << 24) | (datahex[8] << 16) | (datahex[7] << 8) | datahex[6]) / 100.0

        # set converted data to device

        deviceModel.setDeviceData("Pressure", round(Pressure, 0))
        deviceModel.setDeviceData("Height", round(Height, 2))

    def get_gps(self, datahex, deviceModel):
        """
        GPS data
        :param datahex: hex input data
        :param deviceModel: device model
        :return:
        """
        gps_height = deviceModel.get_int(bytes([datahex[2], datahex[3]])) / 10.0
        gps_yaw = deviceModel.get_int(bytes([datahex[4], datahex[5]])) / 100.0
        gps_speed = deviceModel.get_unint(bytes([datahex[6], datahex[7], datahex[8], datahex[9]])) / 1e3

        #TODO: get rid of get_int --> risk adding if statements

        # gps_height = ((datahex[3] << 8) | datahex[2])/10.0
        # gps_yaw = ((datahex[5] << 8) | datahex[4])/100.0
        # gps_speed = ((datahex[9] << 24) | (datahex[8] << 16) | (datahex[7] << 8) | datahex[6])/1e3

        deviceModel.setDeviceData("GPSHeight", round(gps_height, 1))   
        deviceModel.setDeviceData("GPSYaw", round(gps_yaw, 2))   
        deviceModel.setDeviceData("GPSV", round(gps_speed, 3))   

    def get_four_elements(self, datahex, deviceModel):
        """
        get the quaternions
        :param datahex: hex input data
        :param deviceModel: device model
        :return:
        """
        q1 = deviceModel.get_int(bytes([datahex[2], datahex[3]])) / 32768.0
        q2 = deviceModel.get_int(bytes([datahex[4], datahex[5]])) / 32768.0
        q3 = deviceModel.get_int(bytes([datahex[6], datahex[7]])) / 32768.0
        q4 = deviceModel.get_int(bytes([datahex[8], datahex[9]])) / 32768.0

        

        deviceModel.setDeviceData("Q0", round(q1, 5))   # 设备模型元素1赋值
        deviceModel.setDeviceData("Q1", round(q2, 5))   # 设备模型元素2赋值
        deviceModel.setDeviceData("Q2", round(q3, 5))   # 设备模型元素3赋值
        deviceModel.setDeviceData("Q3", round(q4, 5))  # 设备模型元素4赋值

    def get_positioning_accuracy(self, datahex, deviceModel):
        """
        positioning accuracy
        :param datahex: hex input data
        :param deviceModel: device model
        :return:
        """
        SVNUM = deviceModel.get_int(bytes([datahex[2], datahex[3]]))
        PDOP = deviceModel.get_int(bytes([datahex[4], datahex[5]])) / 100.0
        HDOP = deviceModel.get_int(bytes([datahex[6], datahex[7]])) / 100.0
        VDOP = deviceModel.get_int(bytes([datahex[8], datahex[9]])) / 100.0
        

        deviceModel.setDeviceData("SVNUM", round(SVNUM, 0))
        deviceModel.setDeviceData("PDOP", round(PDOP, 2))
        deviceModel.setDeviceData("HDOP", round(HDOP, 2))
        deviceModel.setDeviceData("VDOP", round(VDOP, 2))

    def get_chiptime(self, datahex, deviceModel):
        """
        chip time data
        :param datahex: hex input data
        :param deviceModel: device model
        :return:
        """

        #removed for loop by direclty computing using bitwise operations

        # tempVals = [] 
        # for i in range(4):
        #     tIndex = 2 + i * 2
        #     tempVals.append(datahex[tIndex+1] << 8 | datahex[tIndex])


        # i = 0: datahex[3] << 8 | datahex[2]
        # i = 1: datahex[5] << 8 | datahex[4]
        # i = 2: datahex[7] << 8 | datahex[6]
        # i = 3: datahex[9] << 8 | datahex[8]

        _year = 2000 + ((datahex[3] << 8 | datahex[2]) & 0xff)      
        _moth = (((datahex[3] << 8 | datahex[2]) >> 8) & 0xff)
        _day = ((datahex[5] << 8 | datahex[4]) & 0xff)
        _hour = (((datahex[5] << 8 | datahex[4]) >> 8) & 0xff)
        _minute = ((datahex[7] << 8 | datahex[6]) & 0xff)
        _second = (((datahex[7] << 8 | datahex[6]) >> 8) & 0xff)
        _millisecond = datahex[9] << 8 | datahex[8]
        deviceModel.setDeviceData("Chiptime",
                                  str(_year) + "-" + str(_moth) + "-" + str(_day) + " " + str(_hour) + ":" + str(
                                      _minute) + ":" + str(_second) + "." + str(_millisecond))

    def readReg(self, regAddr, regCount, waitTime, deviceModel):
        """
        read register adress
        :param regAddr: register address
        :param regCount: number of register to read
        :param waitTime: wait time
        :param deviceModel: device model
        :return:
        """
        bret = False
        readCount = int(regCount/4)
        if (regCount % 4>0):
            readCount+=1
        for n in range(readCount):
            self.TempFindValues = []
            tempBytes = self.get_readbytes(regAddr + n * 4)
            success_bytes = self.sendData(tempBytes, deviceModel)
            for i in range(0, 100): # 设置超时1秒
                time.sleep(0.05)  # 休眠50毫秒
                # print(str(i)+","+ str(len(self.TempFindValues)) +"=" + str(regCount))
                if len(self.TempFindValues) >= regCount:    # 已返回所找查的寄存器的值
                    bret = True
                    break
                # 超出等待时间
                if waitTime < i * 0.05 * 1000 :
                    break
        return bret

    def writeReg(self, regAddr, sValue, deviceModel):
        """
        写入寄存器
        :param regAddr: 寄存器地址
        :param sValue: 写入值
        :param deviceModel: 设备模型
        :return:
        """
        tempBytes = self.get_writebytes(regAddr, sValue)                  #获取写入指令
        success_bytes = deviceModel.serialPort.write(tempBytes)          #写入寄存器
    def unlock(self, deviceModel):
        """
        解锁
        :return:
        """
        tempBytes = self.get_writebytes(0x69, 0xb588)                    #获取写入指令
        success_bytes = deviceModel.serialPort.write(tempBytes)          #写入寄存器

    def save(self, deviceModel):
        """
        保存
        :param deviceModel: 设备模型
        :return:
        """
        tempBytes = self.get_writebytes(0x00, 0x00)                      #获取写入指令
        success_bytes = deviceModel.serialPort.write(tempBytes)          #写入寄存器

    def AccelerationCalibration(self, deviceModel):
        """
        加计校准
        :param deviceModel: 设备模型
        :return:
        """
        self.unlock(deviceModel)                                         # 解锁
        time.sleep(0.1)                                                  # 休眠100毫秒
        tempBytes = self.get_writebytes(0x01, 0x01)                      # 获取写入指令
        success_bytes = deviceModel.serialPort.write(tempBytes)          # 写入寄存器
        time.sleep(5.5)                                                  # 休眠5500毫秒

    def BeginFiledCalibration(self, deviceModel):
        """
        开始磁场校准
        :param deviceModel: 设备模型
        :return:
        """
        self.unlock(deviceModel)                                         # 解锁
        time.sleep(0.1)                                                  # 休眠100毫秒
        tempBytes = self.get_writebytes(0x01, 0x07)                      # 获取写入指令 磁场校准
        success_bytes = deviceModel.serialPort.write(tempBytes)          # 写入寄存器

    def EndFiledCalibration(self, deviceModel):
        """
        结束磁场校准
        :param deviceModel: 设备模型
        :return:
        """
        self.unlock(deviceModel)                                         # 解锁
        time.sleep(0.1)                                                  # 休眠100毫秒
        self.save(deviceModel)                                           #保存

    def get_find(self, datahex, deviceModel):
        """
        读取指定寄存器结算
        :param datahex: 原始始数据包
        :param deviceModel: 设备模型
        :return:
        """
        t0l = datahex[2]
        t0h = datahex[3]
        t1l = datahex[4]
        t1h = datahex[5]
        t2l = datahex[6]
        t2h = datahex[7]
        t3l = datahex[8]
        t3h = datahex[9]

        val0 = (t0h << 8 | t0l)
        val1 = (t1h << 8 | t1l)
        val2 = (t2h << 8 | t2l)
        val3 = (t3h << 8 | t3l)
        if self.iFindStartReg > -1:
            deviceModel.setDeviceData(deviceModel.decToHex(self.iFindStartReg), val0)
            deviceModel.setDeviceData(deviceModel.decToHex(self.iFindStartReg + 1), val1)
            deviceModel.setDeviceData(deviceModel.decToHex(self.iFindStartReg + 2), val2)
            deviceModel.setDeviceData(deviceModel.decToHex(self.iFindStartReg + 3), val3)
        self.TempFindValues.extend([val0, val1, val2, val3])