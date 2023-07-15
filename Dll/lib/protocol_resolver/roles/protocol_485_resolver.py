# coding:UTF-8
import time
import datetime
from Dll.lib.protocol_resolver.interface.i_protocol_resolver import IProtocolResolver

"""
    485协议解析器
"""

class Protocol485Resolver(IProtocolResolver):
    #region   计算CRC
    auchCRCHi = [
        0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
        0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
        0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01,
        0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
        0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81,
        0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
        0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01,
        0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
        0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
        0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
        0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01,
        0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
        0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
        0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
        0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01,
        0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
        0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
        0x40]
    auchCRCLo = [
        0x00, 0xC0, 0xC1, 0x01, 0xC3, 0x03, 0x02, 0xC2, 0xC6, 0x06, 0x07, 0xC7, 0x05, 0xC5, 0xC4,
        0x04, 0xCC, 0x0C, 0x0D, 0xCD, 0x0F, 0xCF, 0xCE, 0x0E, 0x0A, 0xCA, 0xCB, 0x0B, 0xC9, 0x09,
        0x08, 0xC8, 0xD8, 0x18, 0x19, 0xD9, 0x1B, 0xDB, 0xDA, 0x1A, 0x1E, 0xDE, 0xDF, 0x1F, 0xDD,
        0x1D, 0x1C, 0xDC, 0x14, 0xD4, 0xD5, 0x15, 0xD7, 0x17, 0x16, 0xD6, 0xD2, 0x12, 0x13, 0xD3,
        0x11, 0xD1, 0xD0, 0x10, 0xF0, 0x30, 0x31, 0xF1, 0x33, 0xF3, 0xF2, 0x32, 0x36, 0xF6, 0xF7,
        0x37, 0xF5, 0x35, 0x34, 0xF4, 0x3C, 0xFC, 0xFD, 0x3D, 0xFF, 0x3F, 0x3E, 0xFE, 0xFA, 0x3A,
        0x3B, 0xFB, 0x39, 0xF9, 0xF8, 0x38, 0x28, 0xE8, 0xE9, 0x29, 0xEB, 0x2B, 0x2A, 0xEA, 0xEE,
        0x2E, 0x2F, 0xEF, 0x2D, 0xED, 0xEC, 0x2C, 0xE4, 0x24, 0x25, 0xE5, 0x27, 0xE7, 0xE6, 0x26,
        0x22, 0xE2, 0xE3, 0x23, 0xE1, 0x21, 0x20, 0xE0, 0xA0, 0x60, 0x61, 0xA1, 0x63, 0xA3, 0xA2,
        0x62, 0x66, 0xA6, 0xA7, 0x67, 0xA5, 0x65, 0x64, 0xA4, 0x6C, 0xAC, 0xAD, 0x6D, 0xAF, 0x6F,
        0x6E, 0xAE, 0xAA, 0x6A, 0x6B, 0xAB, 0x69, 0xA9, 0xA8, 0x68, 0x78, 0xB8, 0xB9, 0x79, 0xBB,
        0x7B, 0x7A, 0xBA, 0xBE, 0x7E, 0x7F, 0xBF, 0x7D, 0xBD, 0xBC, 0x7C, 0xB4, 0x74, 0x75, 0xB5,
        0x77, 0xB7, 0xB6, 0x76, 0x72, 0xB2, 0xB3, 0x73, 0xB1, 0x71, 0x70, 0xB0, 0x50, 0x90, 0x91,
        0x51, 0x93, 0x53, 0x52, 0x92, 0x96, 0x56, 0x57, 0x97, 0x55, 0x95, 0x94, 0x54, 0x9C, 0x5C,
        0x5D, 0x9D, 0x5F, 0x9F, 0x9E, 0x5E, 0x5A, 0x9A, 0x9B, 0x5B, 0x99, 0x59, 0x58, 0x98, 0x88,
        0x48, 0x49, 0x89, 0x4B, 0x8B, 0x8A, 0x4A, 0x4E, 0x8E, 0x8F, 0x4F, 0x8D, 0x4D, 0x4C, 0x8C,
        0x44, 0x84, 0x85, 0x45, 0x87, 0x47, 0x46, 0x86, 0x82, 0x42, 0x43, 0x83, 0x41, 0x81, 0x80,
        0x40]
    #endregion  计算CRC
    TempBytes = []         # 临时数据列表
    gyroRange = 2000.0   # 角速度量程
    accRange = 16.0      # 加速度量程
    angleRange = 180.0   # 角度量程
    TempFindValues = []    # 读取指定寄存器返回的数据
    iFindStartReg = -1  # 读取的首个寄存器

    def get_crc(self, datas, dlen):
        """
        获取CRC校验
        :param datas:数据
        :param dlen:校验数据长度
        :return:
        """
        tempH = 0xff         #高 CRC 字节初始化
        tempL= 0xff         #低 CRC 字节初始化
        for i in range(0, dlen):
            tempIndex = (tempH ^ datas[i]) & 0xff
            tempH = (tempL ^ self.auchCRCHi[tempIndex]) & 0xff
            tempL = self.auchCRCLo[tempIndex]
        return (tempH << 8) | tempL
        pass
    def setConfig(self, deviceModel):
        pass

    def sendData(self, sendData, deviceModel):
        if len(sendData) > 4:
            if sendData[1] == 0x03:
                self.iFindStartReg = sendData[3]
        success_bytes = deviceModel.serialPort.write(sendData)
    def passiveReceiveData(self, data, deviceModel):
        """
        接收数据处理
        :param data: 串口数据
        :param deviceModel: 设备模型
        :return:
        """
        global TempBytes
        for val in data:
            self.TempBytes.append(val)
            if self.TempBytes[0] != deviceModel.ADDR:       # 开头的字节不等于设备ID
                del self.TempBytes[0]                       # 去除第一个字节
                continue
            if len(self.TempBytes) > 2:
                if self.TempBytes[1] != 0x03:            # 第三个字节数值不等于0x03
                    del self.TempBytes[0]                         # 去除第一个字节
                    continue
                tlen = len(self.TempBytes)                        # 获取当前数据长度
                if tlen == self.TempBytes[2] + 5:                 # 表示一个包的数据大小
                    tempCrc = self.get_crc(self.TempBytes, tlen-2)      # 获取CRC校验
                    if (tempCrc >> 8) == self.TempBytes[tlen-2] and (tempCrc & 0xff) == self.TempBytes[tlen-1]:   # 数据CRC校验通过
                        if deviceModel.ReadRegCount * 2 + 5 == tlen:                 # 自动读取的数据
                            self.get_data(self.TempBytes, deviceModel)      # 结算数据
                            deviceModel.dataProcessor.onUpdate(deviceModel) # 触发数据更新事件
                        else:
                            self.get_find(self.TempBytes, deviceModel)
                        self.TempBytes=[]                        #清除数据
                    else:                                        #数据CRC校验未通过
                        del self.TempBytes[0]                    #去除第一个字节

    def get_readbytes(self, devid, regAddr, regCount):
        """
        获取读取的指令
        :param devid: 设备ID
        :param regAddr: 寄存器地址
        :param regCount: 寄存器个数
        :return:
        """
        tempBytes = [None] * 8
        tempBytes[0] = devid                            #设备ID
        tempBytes[1] = 0x03                             #读取指令
        tempBytes[2] = regAddr >> 8                     #寄存器起始位——高位
        tempBytes[3] = regAddr & 0xff                   #寄存器起始位——低位
        tempBytes[4] = regCount >> 8                    #寄存器个数——高位
        tempBytes[5] = regCount & 0xff                  #寄存器个数——低位
        tempCrc = self.get_crc(tempBytes, len(tempBytes)-2)   #获取CRC校验
        tempBytes[6] = tempCrc >> 8                     #CRC校验——高位
        tempBytes[7] = tempCrc & 0xff                   #CRC校验——低位
        return tempBytes

    def get_writebytes(self, devid, regAddr, sValue):
        """
        获取写入的指令
        :param devid: 设备ID
        :param regAddr: 寄存器地址
        :param sValue: 写入的值
        :return:
        """
        tempBytes = [None] * 8
        tempBytes[0] = devid                            #设备ID
        tempBytes[1] = 0x06                             #写入指令
        tempBytes[2] = regAddr >> 8                     #寄存器起始位——高位
        tempBytes[3] = regAddr & 0xff                   #寄存器起始位——低位
        tempBytes[4] = sValue >> 8                      #寄存器数值——高位
        tempBytes[5] = sValue & 0xff                    #寄存器数值——低位
        tempCrc = self.get_crc(tempBytes, len(tempBytes)-2)   #获取CRC校验
        tempBytes[6] = tempCrc >> 8
        tempBytes[7] = tempCrc & 0xff
        return tempBytes

    def get_data(self, datahex, deviceModel):
        """
        calculating the data
        :param datahex: raw data
        :param deviceModel: device model
        :return:
        """
        tempReg = deviceModel.StartReadReg                                  # init of register
        dlen = int(datahex[2] / 2)                                          # num of registers
        tempVals = []                                                       # temp array
        
        for i in range(dlen):
            tempIndex = 3 + i * 2                                           # find the current index
            tempVal = datahex[tempIndex] << 8 | datahex[tempIndex + 1]      # convert the data
            if tempReg == 0x2e:
                deviceModel.setDeviceData("VersionNumber", tempVal)  # setting the version number for the device model
            elif (tempReg >= 0x30 and tempReg <= 0x33):
                # computing time on sensor
                tempVals.append(tempVal)
                if tempReg == 0x33:
                    _year = 2000 + (tempVals[0] & 0xff)
                    _month = ((tempVals[0] >> 8) & 0xff)
                    _day = (tempVals[1] & 0xff)
                    _hour = ((tempVals[1] >> 8) & 0xff)
                    _minute = (tempVals[2] & 0xff)    
                    _second = ((tempVals[2] >> 8) & 0xff)  
                    _millisecond = tempVals[3]             
                    deviceModel.setDeviceData("Chiptime", str(_year) + "-" + str(_month) + "-" + str(_day) + " " + str(_hour) + ":" + str(_minute) + ":" + str(_second) + "." + str(_millisecond))         # 设备模型芯片时间赋值
                    tempVals = []                                           # resetting the data
            elif (tempReg >= 0x34 and tempReg <= 0x36):
                # Acceleration on X Y and Z
                tempVal = tempVal / 32768.0 * self.accRange     #converting the data
                if tempVal >= self.accRange:
                    tempVal -= 2 * self.accRange
                tempVal = round(tempVal, 4)
                if tempReg == 0x34:
                    deviceModel.setDeviceData("AccX", tempVal)
                elif tempReg == 0x35:
                    deviceModel.setDeviceData("AccY", tempVal)
                else:
                    deviceModel.setDeviceData("AccZ", tempVal)
            elif tempReg == 0x40:
                # 温度
                Temperature = round(tempVal/100.0, 2)                       # 温度结算,并保留两位小数
                deviceModel.setDeviceData("Temperature", Temperature)       # 设备模型温度赋值
            elif (tempReg >= 0x37 and tempReg <= 0x39):
                # 角速度X Y Z
                tempVal = tempVal / 32768.0 * self.gyroRange                #角速度结算
                if tempVal >= self.gyroRange:
                    tempVal -= 2 * self.gyroRange
                # 角速度X Y Z赋值
                tempVal = round(tempVal, 4)
                # 设备模型角速度赋值
                if tempReg == 0x37:
                    deviceModel.setDeviceData("GyroX", tempVal)
                elif tempReg == 0x38:
                    deviceModel.setDeviceData("GyroY", tempVal)
                else:
                    deviceModel.setDeviceData("GyroZ", tempVal)
            elif (tempReg >= 0x3d and tempReg <= 0x3f):
                # 角度X Y Z
                tempVal = tempVal / 32768.0 * self.angleRange                  #角度结算
                if tempVal >= self.angleRange:
                    tempVal -= 2 * self.angleRange
                # 设备模型角度X Y Z赋值
                tempVal = round(tempVal, 3)
                # 设备模型角度X赋值
                if tempReg == 0x3d:
                    deviceModel.setDeviceData("AngleX", tempVal)
                elif tempReg == 0x3e:
                    deviceModel.setDeviceData("AngleY", tempVal)
                else:
                    deviceModel.setDeviceData("AngleZ", tempVal)
            elif (tempReg >= 0x3a and tempReg <= 0x3c):
                # 磁场X Y Z
                # 设备模型磁场赋值
                if tempReg == 0x3a:
                    deviceModel.setDeviceData("MagX", tempVal)
                elif tempReg == 0x3b:
                    deviceModel.setDeviceData("MagY", tempVal)
                else:
                    deviceModel.setDeviceData("MagZ", tempVal)
            elif (tempReg >= 0x41 and tempReg <= 0x44):
                # 端口
                # 设备模型端口赋值
                if tempReg == 0x41:
                    deviceModel.setDeviceData("D0", tempVal)
                elif tempReg == 0x42:
                    deviceModel.setDeviceData("D1", tempVal)
                elif tempReg == 0x43:
                    deviceModel.setDeviceData("D2", tempVal)
                else:
                    deviceModel.setDeviceData("D3", tempVal)
            elif (tempReg == 0x49 or tempReg == 0x4b):
                # 经纬度
                # 设备模型经纬度赋值
                if tempReg == 0x49:
                    lon = deviceModel.get_unint(bytes([datahex[tempIndex+1], datahex[tempIndex], datahex[tempIndex+3], datahex[tempIndex+2]]))
                    tlon = lon / 10000000.0
                    deviceModel.setDeviceData("Lon", round(tlon, 8))  # 设备模型经度赋值
                elif tempReg == 0x4b:
                    lat = deviceModel.get_unint(bytes([datahex[tempIndex+1], datahex[tempIndex], datahex[tempIndex+3], datahex[tempIndex+2]]))
                    tlat = lat / 10000000.0
                    deviceModel.setDeviceData("Lat", round(tlat, 8))  # 设备模型纬度赋值
            elif (tempReg == 0x45 or tempReg == 0x47):
                # 气压和高度
                # 设备模型气压和高度赋值
                if tempReg == 0x45:
                    Pressure = deviceModel.get_unint(bytes([datahex[tempIndex+1], datahex[tempIndex], datahex[tempIndex+3], datahex[tempIndex+2]]))
                    deviceModel.setDeviceData("Pressure", round(Pressure, 0))
                elif tempReg == 0x47:
                    Height = deviceModel.get_unint(bytes([datahex[tempIndex+1], datahex[tempIndex], datahex[tempIndex+3], datahex[tempIndex+2]]))
                    deviceModel.setDeviceData("Height", round(Height, 2))
            elif (tempReg >= 0x4d and tempReg <= 0x4f):
                # GPS
                if tempReg == 0x4d:
                    # 高度
                    Height = tempVal / 10.0
                    deviceModel.setDeviceData("GPSHeight", round(Height, 1))
                elif tempReg == 0x4e:
                    # 航向角
                    Yaw = tempVal / 100.0
                    deviceModel.setDeviceData("GPSYaw", round(Yaw, 2))
                elif tempReg == 0x4f:
                    # 地速  #海里
                    Speed = deviceModel.get_unint(bytes([datahex[tempIndex+1], datahex[tempIndex], datahex[tempIndex+3], datahex[tempIndex+2]])) / 1e3
                    deviceModel.setDeviceData("GPSV", round(Speed, 3))   # 设备模型速度赋值
            elif (tempReg >= 0x51 and tempReg <= 0x54):
                # 四元素
                tempVal = tempVal / 32768.0
                # 设备模型元素赋值
                if tempReg == 0x51:
                    deviceModel.setDeviceData("Q0", round(tempVal, 5))
                elif tempReg == 0x52:
                    deviceModel.setDeviceData("Q1", round(tempVal, 5))
                elif tempReg == 0x53:
                    deviceModel.setDeviceData("Q2", round(tempVal, 5))
                else:
                    deviceModel.setDeviceData("Q3", round(tempVal, 5))
            elif (tempReg >= 0x55 and tempReg <= 0x58):
                # 定位精度
                # 定位精度赋值:卫星数、位置精度、水平精度、垂直精度
                if tempReg == 0x55:
                    SVNUM = tempVal
                    deviceModel.setDeviceData("SVNUM", round(SVNUM, 0))
                elif tempReg == 0x56:
                    PDOP = tempVal / 100.0
                    deviceModel.setDeviceData("PDOP", round(PDOP, 2))
                elif tempReg == 0x57:
                    HDOP = tempVal / 100.0
                    deviceModel.setDeviceData("HDOP", round(HDOP, 2))
                else:
                    VDOP = tempVal / 100.0
                    deviceModel.setDeviceData("VDOP", round(VDOP, 2))
            # 下一个寄存器
            tempReg += 1

    def readReg(self, regAddr, regCount, waitTime, deviceModel):
        """
        读取寄存器
        :param regAddr: 寄存器地址
        :param regCount: 寄存器个数
        :param deviceModel: 设备模型
        :return:
        """
        bret = False
        self.TempFindValues = []                        #清除数据
        self.TempReadRegCount = regCount
        tempBytes = self.get_readbytes(deviceModel.ADDR, regAddr, regCount)         # 获取读取的指令
        success_bytes = self.sendData(tempBytes, deviceModel)   # 写入数据
        if waitTime > 0:
            for i in range(0, 100): # 设置超时1秒
                time.sleep(0.05)  # 休眠50毫秒
                if len(self.TempFindValues) >= regCount:  # 已返回所找查的寄存器的值
                    bret = True
                    break
                # 超出等待时间
                if waitTime < i * 0.05 * 1000:
                    break
        return bret

    def writeReg(self, regAddr,sValue, deviceModel):
        """
        写入寄存器
        :param regAddr: 寄存器地址
        :param sValue: 写入值
        :param deviceModel: 设备模型
        :return:
        """
        tempBytes = self.get_writebytes(deviceModel.ADDR, regAddr, sValue) #获取写入指令
        success_bytes = deviceModel.serialPort.write(tempBytes)          #写入寄存器

    def get_find(self, datahex, deviceModel):
        """
        读取指定寄存器结算
        :param datahex: 原始始数据包
        :param deviceModel: 设备模型
        :return:
        """
        tempArr = []                                                        #临时存储
        dlen = int(datahex[2]/2)                                            #寄存器个数
        for i in range(0, dlen):
            tempIndex = 3 + i * 2                                           #获取当前数据索引
            tempVal = datahex[tempIndex] << 8 | datahex[tempIndex + 1]      #数据转换
            tempArr.append(tempVal)                                        #将数据添加到列表中
            deviceModel.setDeviceData(deviceModel.decToHex(self.iFindStartReg + i), tempVal)

        self.TempFindValues.extend(tempArr)

    def unlock(self, deviceModel):
        """
        解锁
        :return:
        """
        tempBytes = self.get_writebytes(deviceModel.ADDR, 0x69, 0xb588)  # 获取写入指令
        success_bytes = deviceModel.serialPort.write(tempBytes)         # 写入寄存器


    def save(self, deviceModel):
        """
        保存
        :return:
        """
        tempBytes = self.get_writebytes(deviceModel.ADDR, 0x00, 0x00)  # 获取写入指令
        success_bytes = deviceModel.serialPort.write(tempBytes)       #写入寄存器

    def AccelerationCalibration(self, deviceModel):
        """
        加计校准
        :param deviceModel: 设备模型
        :return:
        """
        self.unlock(deviceModel)                                      # 解锁
        time.sleep(0.1)                                               # 休眠100毫秒
        tempBytes = self.get_writebytes(deviceModel.ADDR, 0x01, 0x01)  # 获取写入指令
        success_bytes = deviceModel.serialPort.write(tempBytes)       # 写入寄存器
        time.sleep(5.5)                                               # 休眠5500毫秒

    def BeginFiledCalibration(self,deviceModel):
        """
        开始磁场校准
        :param deviceModel: 设备模型
        :return:
        """
        self.unlock(deviceModel)                                         # 解锁
        time.sleep(0.1)                                                  # 休眠100毫秒
        tempBytes = self.get_writebytes(deviceModel.ADDR, 0x01, 0x07)     # 获取写入指令 磁场校准
        success_bytes = deviceModel.serialPort.write(tempBytes)          # 写入寄存器


    def EndFiledCalibration(self, deviceModel):
        """
        结束磁场校准
        :param deviceModel: 设备模型
        :return:
        """
        self.unlock(deviceModel)                                         # 解锁
        time.sleep(0.1)                                                  # 休眠100毫秒
        self.save(deviceModel)                                           # 保存