import time
import datetime
import platform
import struct
import Dll.lib.device_model as deviceModel
from Dll.lib.data_processor.roles.jy901s_dataProcessor import JY901SDataProcessor
from Dll.lib.protocol_resolver.roles.wit_protocol_resolver import WitProtocolResolver
from Dll.lib.Modular.interface.i_operating_equipment import IOperatingEquipment
"""
JY901设备
"""


class JY901(IOperatingEquipment):
    # 设备
    device = None

    def __init__(self):
        """
        初始化一个设备模型
        :param self:
        :return:
        """
        self.device = deviceModel.DeviceModel(
            "我的JY901",
            WitProtocolResolver(),
            JY901SDataProcessor(),
            "51_0"
        )

    def GetDeviceName(self):
        """
        获得设备名称
        :return:
        """
        return self.device.deviceName

    def SetPortName(self, portName):
        """
        设置串口号
        :param self:
        :param portName:
        :return:
        """
        self.device.serialConfig.portName = portName

    def SetBaudrate(self, baudrate):
        """
        设置波特率
        :param self:
        :param baudrate:
        :return:
        """
        self.device.serialConfig.baud = baudrate

    def Open(self):
        """
        打开设备
        :param self:
        :return:
        """
        self.device.openDevice()
        #self.device.dataProcessor.onVarChanged.append(onUpdate)  # 数据更新事件

    def AddOnRecord(self, eventOnRecord):
        """
        添加事件
        :param eventOnRecord: 接收数据事件
        :return:
        """
        self.device.dataProcessor.onVarChanged.append(eventOnRecord)  # 数据更新事件

    def RemoveOnRecord(self, eventOnRecord):
        """
        移除事件
        :param eventOnRecord: 接收数据事件
        :return:
        """
        self.device.dataProcessor.onVarChanged.remove(eventOnRecord)  # 数据更新事件

    def IsOpen(self):
        """
        串口是否打开
        :return:
        """
        return self.device.isOpen

    def UnlockReg(self):
        """
        解锁寄存器
        :return:
        """
        self.device.unlock()

    def AppliedCalibration(self):
        """
        加计校准
        :return:
        """
        self.device.AppliedCalibration()

    def StartFieldCalibration(self):
        """
        开始磁场校准
        :return:
        """
        self.device.BeginFiledCalibration()

    def EndFieldCalibration(self):
        """
        结束磁场校准
        :return:
        """
        self.device.EndFiledCalibration()

    def SetReturnRate(self, rate):
        """
        设置回传速率
        :param rate:
        :return:
        """
        self.SendWriteReg(0x03, rate)

    def SendReadReg(self, reg, waitTime):
        """
        发送读取寄存器的命令
        :param reg: 寄存器地址
        :param waitTime: 等待时间（毫秒）
        :return:
        """
        return self.device.readReg(reg, 4, waitTime)

    def SendWriteReg(self, reg, data):
        """
        发送读取寄存器的命令
        :param reg: 寄存器地址
        :param data: 寄存器对应的值
        :return:
        """
        return self.device.writeReg(reg, data)

    def SendProtocolData(self, data, waitTime):
        """
        发送带协议的数据
        :param data:
        :param waitTime: 等待时间（毫秒）
        :return:
        """
        self.device.sendData(data)
        time.sleep(waitTime/1000.0)  # 休眠

    def decToHex(self, num):
        """
        10进制转16进制
        :param num:
        :return:
        """
        return self.device.decToHex(num)

    def SaveReg(self):
        """
        保存寄存器
        :return:
        """
        self.device.save()

    def SetReturnRate(self, rate):
        """
        设置回传速率
        :param rate:回传速率
        :return:
        """
        self.device.writeReg(0x03,rate)

    def Close(self):
        """
        关闭设备
        :param self:
        :return:
        """
        self.device.closeDevice()

    def GetDeviceData(self, key):
        """
        获得Key值数据
        :param key:数据键值
        :return:
        """
        tempKey = str(key).upper()
        if str(key).upper().startswith("0X"):
            tempKey=str(key)[2:]

        return self.device.GetDeviceData(tempKey)



